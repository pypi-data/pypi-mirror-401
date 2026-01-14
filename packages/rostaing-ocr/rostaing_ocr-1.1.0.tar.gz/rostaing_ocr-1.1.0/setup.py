from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="rostaing-ocr",
    version="1.1.0",  # Updated version
    author="Rostaing",
    author_email="rostaingdavila@gmail.com", # Replace with your email
    description="A high-precision, layout-preserving OCR extraction tool for PDFs and images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rostaing/rostaing-ocr", # Optional: Add your repo URL
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
    entry_points={
        'console_scripts': [
            # Allows usage: rostaing-ocr mydoc.pdf
            'rostaing-ocr=rostaing_ocr.rostaing_ocr:main', 
        ],
    },
)