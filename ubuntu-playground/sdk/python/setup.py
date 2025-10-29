"""Setup configuration for Ubuntu Playground Python SDK"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ubuntu-playground-sdk",
    version="1.0.0",
    author="Homo Lumen Coalition",
    author_email="noreply@homo-lumen.com",
    description="Python SDK for Ubuntu Playground API with Triadiske Portvokter support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums",
    py_modules=["ubuntu_playground_sdk"],
    classifiers=[
        "Development Status :: 4 - Beta",
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
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="ubuntu-playground triadiske-portvokter biofelt-gate thalos-filter mutation-log homo-lumen",
    project_urls={
        "Bug Reports": "https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/issues",
        "Documentation": "https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/tree/main/ubuntu-playground",
    },
)
