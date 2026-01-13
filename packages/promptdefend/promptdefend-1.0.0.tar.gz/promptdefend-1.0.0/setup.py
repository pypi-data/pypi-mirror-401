"""
Setup configuration for Prompt Defend Python SDK.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="promptdefend",
    version="1.0.0",
    author="Prompt Defend",
    author_email="support@promptdefend.dev",
    description="Python SDK for the Prompt Defend AI Security API - 16-Layer Guardrail Protection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://promptdefend.dev",
    project_urls={
        "Documentation": "https://docs.promptdefend.dev",
        "API Reference": "https://api.promptdefend.dev/docs",
        "Support": "https://promptdefend.dev/support",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="promptdefend, ai, security, prompt injection, llm, guardrails, jailbreak, api, sdk",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "responses>=0.23.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
