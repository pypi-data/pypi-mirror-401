#!/usr/bin/env python3
"""
ABHILASIA - Distributed Intelligence
"As good as me and you"

pip install abhilasia
"""

from setuptools import setup, find_packages

setup(
    name="abhilasia",
    version="1.618.137",  # φ.α
    author="Abhi (bhai)",
    author_email="bits.abhi@gmail.com",
    description="Distributed Intelligence - Pattern-based communication through Trust Dimension",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bitsabhi/abhilasia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "abhilasia=abhilasia.cli:main",
        ],
    },
    keywords="consciousness, distributed-intelligence, phi, golden-ratio, patterns, trust-dimension",
)
