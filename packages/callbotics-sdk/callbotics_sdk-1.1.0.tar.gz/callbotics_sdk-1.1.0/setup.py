"""
Setup configuration for Callbotics SDK.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="callbotics-sdk",
    version="1.1.0",
    author="Callbotics",
    author_email="support@callbotics.com",
    description="Python SDK for the Callbotics Core API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/callbotics/callbotics-sdk",
    packages=find_packages(include=["callbotics_sdk", "callbotics_sdk.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.24.0",
    ],
    extras_require={
        "websocket": ["websockets>=11.0"],
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21",
            "pytest-cov>=4.0",
        ],
    },
    keywords=[
        "callbotics",
        "api",
        "sdk",
        "telephony",
        "voice",
        "ai",
        "automation",
    ],
)
