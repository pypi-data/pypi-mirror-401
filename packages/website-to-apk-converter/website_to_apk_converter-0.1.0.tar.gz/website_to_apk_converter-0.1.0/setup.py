from setuptools import setup, find_packages

setup(
    name="website-to-apk-converter",  # CHANGE THIS: Must be unique on PyPI
    version="0.1.0",
    author="SHAIK JANU",
    author_email="shaiksadikjanu@gmail.com",
    description="A library to convert websites into Android APK files using android sdk and APKTool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,  # Crucial for including assets
    install_requires=[
        "Pillow",  # Your code uses PIL
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)