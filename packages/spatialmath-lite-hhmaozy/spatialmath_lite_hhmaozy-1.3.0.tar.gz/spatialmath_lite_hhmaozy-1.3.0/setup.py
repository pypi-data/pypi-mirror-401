from setuptools import setup, find_packages
import os

# 读取README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本
with open(os.path.join("spatialmath_lite", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="spatialmath-lite",
    version=version,
    author="Hh",
    author_email="ZM7x9@outlook.com",
    description="Ultra-lightweight spatial mathematics with optimized negative number support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hh-dev/spatialmath-lite",
    packages=find_packages(include=["spatialmath_lite", "spatialmath_lite.*"]),
    package_data={
        "spatialmath_lite": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Visualization",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "test": ["pytest>=7.0", "pytest-cov>=4.0"],
        "dev": ["black>=23.0", "mypy>=1.0", "ruff>=0.1", "pytest>=7.0", "pytest-cov>=4.0"],
        "docs": ["sphinx>=7.0", "sphinx-rtd-theme>=1.0"],
    },
    keywords=[
        "spatial",
        "mathematics", 
        "3d",
        "optimized",
        "negative-numbers",
        "edge-computing",
        "embedded",
        "lightweight",
        "numpy",
    ],
    project_urls={
        "Homepage": "https://github.com/hh-dev/spatialmath-lite",
        "Repository": "https://github.com/hh-dev/spatialmath-lite.git",
        "Issues": "https://github.com/hh-dev/spatialmath-lite/issues",
    },
)
