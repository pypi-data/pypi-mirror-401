"""Setup configuration for site2markdown package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="site2markdown",
    version="1.0.0",
    author="Sumit Banik",
    author_email="sumitbanik02@gmail.com",
    description="Convert URL content to markdown for better LLM context.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "html2text>=2020.1.16",
        "readability-lxml>=0.8.1",
    ],
)
