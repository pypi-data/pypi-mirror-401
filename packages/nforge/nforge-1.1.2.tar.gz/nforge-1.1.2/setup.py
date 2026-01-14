"""
NeuralForge setup configuration.
"""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="nforge",
    version="1.1.1",
    author="NeuralForge Team",
    author_email="team@neuralforge.dev",
    description="The ML API Framework - FastAPI for Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rockstream/neuralforge",
    project_urls={
        "Documentation": "https://github.com/rockstream/neuralforge#readme",
        "Source": "https://github.com/rockstream/neuralforge",
        "Bug Reports": "https://github.com/rockstream/neuralforge/issues",
        "Changelog": "https://github.com/rockstream/neuralforge/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings[python]>=0.20.0",
        ],
        "pytorch": [
            "torch>=2.0.0",
            "torchvision>=0.15.0",
        ],
        "tensorflow": [
            "tensorflow>=2.13.0",
        ],
        "onnx": [
            "onnxruntime>=1.15.0",
        ],
        "all": [
            "torch>=2.0.0",
            "tensorflow>=2.13.0",
            "onnxruntime>=1.15.0",
            "transformers>=4.30.0",
            "sentence-transformers>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neuralforge=neuralforge.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
