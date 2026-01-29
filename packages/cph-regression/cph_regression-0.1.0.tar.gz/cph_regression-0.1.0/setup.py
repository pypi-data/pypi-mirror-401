"""
Setup script for cph-regression package.

This is a fallback setup.py for compatibility with older build tools.
Modern builds should use pyproject.toml.
"""

from setuptools import setup, find_packages

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A generic, config-driven regression training package using PyTorch Lightning"

setup(
    name="cph-regression",
    version="0.1.0",
    author="chandra",
    author_email="chandra385123@gmail.com",
    description="A generic, config-driven regression training package using PyTorch Lightning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imchandra11/cph-regression",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "lightning>=2.1.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "Pillow>=9.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "joblib>=1.3.0",
        "onnx>=1.14.0",
        "onnxruntime>=1.16.0,<1.23.0",
        "torchmetrics>=1.0.0",
        "pyyaml>=6.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "jinja2>=3.1.0",
        "python-multipart>=0.0.6",
        "pydantic>=2.0.0",
        "tensorboard>=2.13.0",
        "jsonargparse[signatures]>=4.27.7",
    ],
    entry_points={
        "console_scripts": [
            "cph-regression=cph_regression.cli:main",
        ],
    },
)
