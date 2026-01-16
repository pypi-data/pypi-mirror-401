from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="apk-website-converter",  # unique name for PyPI
    version="0.1.1",
    author="SHAIKJANU",
    author_email="shaikjanu08012007@gmail.com",
    description="A library to convert website URLs into Android APKs using Apktool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaiksadikjanu/apk-builder", # Optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Pillow",  # We rely on PIL for image processing
    ],
    # This is critical: it tells setup to look at MANIFEST.in
    include_package_data=True, 
)