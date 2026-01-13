"""
FireVM Python SDK
A Python client library for the FireVM microVM management platform.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="firevm",
    version="0.4.0",
    author="FireVM Team",
    author_email="support@firevm.dev",
    description="Official Python SDK for FireVM - MicroVM Management Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firevm/firevm-python",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
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
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "async": ["aiohttp>=3.9.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
            "ruff>=0.1.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/firevm/firevm-python/issues",
        "Documentation": "https://docs.firevm.dev",
        "Source": "https://github.com/firevm/firevm-python",
    },
)
