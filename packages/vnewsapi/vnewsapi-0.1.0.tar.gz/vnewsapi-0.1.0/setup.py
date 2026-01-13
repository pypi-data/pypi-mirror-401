"""
Setup script for vnewsapi package.
Legacy setup.py for compatibility.
"""

from setuptools import setup, find_packages

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A Python library for crawling Vietnamese financial news"

setup(
    name="vnewsapi",
    version="0.1.0",
    author="vnewsapi contributors",
    author_email="support@vnewsapi.com",
    description="A Python library for crawling Vietnamese financial news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hoanganhvu123/vnewsapi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "feedparser>=6.0.0",
        "html2text>=2020.1.16",
        "pandas>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
        ],
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
)

