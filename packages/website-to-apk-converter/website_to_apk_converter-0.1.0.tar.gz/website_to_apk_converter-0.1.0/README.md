# Website to APK Converter

A Python library to convert website URLs into native Android APK files.

## Installation

```bash
pip install website-to-apk-converter
Usage
Python

from apk_builder import APKConverter

config = {
    "android_sdk_path": "/path/to/android/sdk/build-tools/34.0.0",
    "apktool_path": "/path/to/apktool.jar",
    # Optional: custom base apk or keystore
}

converter = APKConverter(config)

converter.generate_apk(
    url="[https://google.com](https://google.com)",
    app_name="GoogleApp",
    icon_path="icon.png",
    splash_logo_path="logo.png",
    splash_bg_path="bg.png",
    output_dir="./output"
)
Requirements:

Java installed (for APKTool)

Android SDK Build Tools (for zipalign/apksigner)