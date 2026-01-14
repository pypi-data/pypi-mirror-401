from setuptools import setup, find_packages
import os

# Robust way to read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rostaing-ocr",
    version="1.1.1",  # INCREMENTED VERSION (Mandatory for PyPI update)
    author="Rostaing",
    author_email="rostaingdavilaemail@gmail.com", # Remplacez ceci
    description="A high-precision, layout-preserving OCR extraction tool for PDFs and images.",
    long_description=long_description,
    long_description_content_type="text/markdown", # Crucial for PyPI to render MD
    url="https://github.com/Rostaing/rostaing-ocr", # Optionnel
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pymupdf>=1.20.0",
        "easyocr>=1.7.0",
        "pillow>=9.0.0",
        "numpy>=1.21.0",
    ],
    # This ensures files in MANIFEST.in are included
    include_package_data=True, 
)