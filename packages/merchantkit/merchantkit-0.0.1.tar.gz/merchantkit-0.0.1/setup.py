"""
Minimal setup.py to claim 'merchantkit' name on PyPI

This is a placeholder package to reserve the name while full package is developed.
DO NOT use this in production yet.
"""

import os
from setuptools import setup, find_packages

# Read README for long description
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="merchantkit",
    version="0.0.1",
    author="MerchantKit Contributors",
    author_email="merchantkit@example.com",
    description="E-commerce operations toolkit for Python (in development)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merchantkit/merchantkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
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
        # Will be populated as package develops
    ],
    keywords="ecommerce commerce toolkit merchant orders fulfillment inventory catalog shipping",
    project_urls={
        "Documentation": "https://github.com/merchantkit/merchantkit",
        "Source": "https://github.com/merchantkit/merchantkit",
        "Tracker": "https://github.com/merchantkit/merchantkit/issues",
    },
)
