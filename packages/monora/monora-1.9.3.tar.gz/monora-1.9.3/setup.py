"""Setup configuration for Monora SDK."""
import atexit
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop


def _post_install():
    """Show post-installation message."""
    # Delay import to avoid issues during install
    try:
        from monora._postinstall import post_install
        post_install()
    except Exception:
        # Fallback message if import fails
        print("\n📦 Monora SDK installed successfully!")
        print("   Run 'monora init' to configure.\n")


class PostInstallCommand(install):
    """Custom install command that shows post-install message."""

    def run(self):
        install.run(self)
        # Use atexit to show message after all installation is complete
        atexit.register(_post_install)


class PostDevelopCommand(develop):
    """Custom develop command that shows post-install message."""

    def run(self):
        develop.run(self)
        atexit.register(_post_install)


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="monora",
    version="1.9.3",
    author="Monora Team",
    author_email="info@monora.ai",
    description="Lightweight governance and trace SDK for AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monora/monora",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*", "monora-node", "monora-node.*"]),
    include_package_data=True,
    package_data={
        "monora": ["*.json", "schemas/*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click>=8.0.0",
        "jsonschema>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
        "yaml": [
            "pyyaml>=6.0",
        ],
        "https": [
            "requests>=2.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "monora=monora.cli.report:cli",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
)
