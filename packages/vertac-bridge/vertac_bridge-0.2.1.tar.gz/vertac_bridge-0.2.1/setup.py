#!/usr/bin/env python3
"""
VerTac Sensor Data Bridge Setup Script
Standalone bridge for sensor data ingestion
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vertac-bridge",
    version="0.2.1",
    author="VerTac Team",
    author_email="info@vertac.dev",
    description="VerTac Sensor Data Bridge - Lightweight connector for sensor data ingestion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/vertac-bridge",
    packages=find_packages(include=["desktop_bridge*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "vertac-bridge=desktop_bridge.sensor_bridge:main",
        ],
    },
)
