"""
Setup script for text-quality-analyzer package
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="text-quality-analyzer",
    version="0.1.1",
    author="Text Quality Analyzer Team",
    author_email="your.email@example.com",
    description="Universal text analysis module for detecting language, meaningfulness, and structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/text-quality-analyzer",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langid>=1.1.6",
        "textstat>=0.7.3",
        "wordfreq>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "text-quality-analyzer=text_quality_analyzer.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
