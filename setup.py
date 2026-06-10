#!/usr/bin/env python3
"""SmartScraper - Zero-config intelligent web scraping framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smartscraper-cli",
    version="1.0.0",
    author="Gitstq",
    author_email="",
    description="Zero-config intelligent web scraping framework with AI-powered selectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/smartscraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "fake-useragent>=1.4.0",
        "urllib3>=1.26.0",
    ],
    extras_require={
        "ai": ["openai>=1.0.0", "httpx>=0.24.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "smartscraper=smartscraper.cli:main",
            "ss=smartscraper.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
