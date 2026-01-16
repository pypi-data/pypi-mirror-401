import os
import json
import shutil
import subprocess
import uuid
import platform
import random
import string
import re
import glob 
from PIL import Image 

class APKConverter:
    def __init__(self, config):
        """
        Initialize the converter with necessary paths.
        config dictionary should contain:
        - android_sdk_path
        - apktool_path
        - keystore_path
        - keystore_pass
        - key_alias
        - base_apk_path
        """
        self.ANDROID_BUILD_TOOLS = config.get('android_sdk_path')
        self.APKTOOL_JAR_PATH = config.get('apktool_path')
        self.KEYSTORE_PATH = config.get('keystore_path')
        self.KEYSTORE_PASS = config.get('keystore_pass')
        self.KEY_ALIAS = config.get('key_alias')
        self.BASE_APK_PATH = config.get('base_apk_path')
        
        # Verify tools immediately
        self.zipalign_path, self.apksigner_path = self._verify_tools_exist()

    def _verify_tools_exist(self):
        ext = ".exe" if platform.system() == "Windows" else ""
        bat = ".bat" if platform.system() == "Windows" else ""
        
        zipalign_path = os.path.join(self.ANDROID_BUILD_TOOLS, f"zipalign{ext}")
        apksigner_path = os.path.join(self.ANDROID_BUILD_TOOLS, f"apksigner{bat}")

        if not os.path.exists(zipalign_path): 
            raise FileNotFoundError(f"Missing zipalign at {zipalign_path}")
        if not os.path.exists(apksigner_path): 
            raise FileNotFoundError(f"Missing apksigner at {apksigner_path}")
        if not os.path.exists(self.APKTOOL_JAR_PATH): 
            raise FileNotFoundError(f"Missing apktool.jar at {self.APKTOOL_JAR_PATH}")
        if not os.path.exists(self.BASE_APK_PATH):
            raise FileNotFoundError(f"Missing base.apk at {self.BASE_APK_PATH}")

        return zipalign_path, apksigner_path

    def _clean_conflicting_resources(self, directory, resource_name):
        pattern = os.path.join(directory, f"{resource_name}.*")
        files = glob.glob(pattern)
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Warning: Could not delete {f}: {e}")

    def _process_image(self, image_input, directory, resource_name, resize_dim=None):
        self._clean_conflicting_resources(directory, resource_name)
        target_path = os.path.join(directory, f"{resource_name}.png")
        
        try:
            # Open image (supports both file paths and bytes/streams)
            img = Image.open(image_input)
            img = img.convert("RGBA")
            if resize_dim:
                img = img.resize(resize_dim, Image.Resampling.LANCZOS)
            img.save(target_path, "PNG")
        except Exception as e:
            raise Exception(f"Error processing image {resource_name}: {e}")

    def _run_apktool_decode(self, apk_path, output_dir):
        cmd = ["java", "-jar", self.APKTOOL_JAR_PATH, "d", "-f", "--no-src", "-o", output_dir, apk_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    def _run_apktool_build(self, source_dir, output_apk):
        cmd = ["java", "-jar", self.APKTOOL_JAR_PATH, "b", "-o", output_apk, source_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Apktool Build Failed: {result.stderr}")

    def _safe_manifest_update(self, decoded_dir, new_package_name):
        manifest_path = os.path.join(decoded_dir, "AndroidManifest.xml")
        if not os.path.exists(manifest_path): return

        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'package="([^"]+)"', content)
        if not match: return
        old_package = match.group(1)
        
        # Replacements
        content = re.sub(r'android:name="\.', f'android:name="{old_package}.', content)
        content = content.replace(f'package="{old_package}"', f'package="{new_package_name}"')
        content = content.replace(f'android:authorities="{old_package}', f'android:authorities="{new_package_name}')
        
        # Ensure native libs extract is true if present
        if 'android:extractNativeLibs="false"' in content:
            content = content.replace('android:extractNativeLibs="false"', 'android:extractNativeLibs="true"')

        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update apktool.yml
        yml_path = os.path.join(decoded_dir, "apktool.yml")
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                yml = f.read()
            if "renameManifestPackage:" in yml:
                 yml = re.sub(r'(renameManifestPackage:\s*)(.*)', fr'\1{new_package_name}', yml)
            else:
                 yml += f"\nrenameManifestPackage: {new_package_name}\n"
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.write(yml)

    def _update_app_name_label(self, decoded_dir, new_app_name):
        paths = [
            os.path.join(decoded_dir, "res", "values", "strings.xml"),
            os.path.join(decoded_dir, "res", "values-en", "strings.xml")
        ]
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read()
                pattern = r'(<string[^>]*name="app_name"[^>]*>)(.*?)(</string>)'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, fr'\1{new_app_name}\3', content)
                    with open(p, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return

    def generate_apk(self, url, app_name, icon_path, splash_logo_path, splash_bg_path, output_dir, splash_time=3000):
        """
        Main function to generate the APK.
        Returns the path to the final generated APK.
        """
        # We generate a random package name for internal uniqueness
        package_name = f"com.gen.a{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
        unique_id = str(uuid.uuid4())[:8]
        
        # Temporary working directory (Hidden inside the output dir or temp)
        work_dir = os.path.join(output_dir, "temp_" + unique_id)
        decoded_dir = os.path.join(work_dir, "decoded")
        rebuilt_apk = os.path.join(work_dir, "rebuilt.apk")
        
        # Clean the App Name for the final file
        clean_name = app_name if app_name.endswith('.apk') else f"{app_name}.apk"
        final_apk_path = os.path.join(output_dir, clean_name)

        try:
            os.makedirs(decoded_dir, exist_ok=True)
            
            # 1. Decode
            print(f"Decoding base APK...")
            self._run_apktool_decode(self.BASE_APK_PATH, decoded_dir)

            # 2. Update Manifest & Name
            self._safe_manifest_update(decoded_dir, package_name)
            self._update_app_name_label(decoded_dir, app_name)

            # 3. Process Images
            print(f"Processing images...")
            drawable_dir = os.path.join(decoded_dir, "res", "drawable")
            os.makedirs(drawable_dir, exist_ok=True)
            
            self._process_image(icon_path, drawable_dir, "app_icon", resize_dim=(192, 192))
            self._process_image(splash_logo_path, drawable_dir, "splash_logo")
            self._process_image(splash_bg_path, drawable_dir, "splash_bg")

            # 4. Config JSON
            config_data = {
                "url": url, 
                "appName": app_name,
                "splash_time": int(splash_time)
            }
            config_path = os.path.join(decoded_dir, "assets", "config.json")
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)

            # 5. Build, Align, Sign
            print(f"Building APK...")
            self._run_apktool_build(decoded_dir, rebuilt_apk)
            
            print(f"Aligning and Signing...")
            
            # Remove existing file if it exists so we don't get errors
            if os.path.exists(final_apk_path):
                try:
                    os.remove(final_apk_path)
                except Exception as e:
                    print(f"Warning: Could not remove existing file {final_apk_path}: {e}")

            subprocess.run([self.zipalign_path, "-p", "-f", "-v", "4", rebuilt_apk, final_apk_path], check=True, stdout=subprocess.DEVNULL)
            
            subprocess.run([
                self.apksigner_path, "sign",
                "--ks", self.KEYSTORE_PATH,
                "--ks-pass", f"pass:{self.KEYSTORE_PASS}",
                "--key-pass", f"pass:{self.KEYSTORE_PASS}",
                "--ks-key-alias", self.KEY_ALIAS,
                final_apk_path
            ], check=True, stdout=subprocess.DEVNULL)

            print(f"Success! APK saved at: {final_apk_path}")
            return final_apk_path

        except Exception as e:
            print(f"Error during generation: {e}")
            raise e
        finally:
            # Cleanup temp files
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir, ignore_errors=True)