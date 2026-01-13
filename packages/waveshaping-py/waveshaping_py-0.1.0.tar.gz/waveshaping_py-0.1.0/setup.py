"""
Setup script for waveshaping-py package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="waveshaping-py",
    version="0.1.0",
    author="Tsuguma Sayutani",
    author_email="",
    description="Python library for audio waveshaping and distortion effects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsugumasa320/waveshaping-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
        "examples": [
            "matplotlib>=3.3.0",
            "soundfile>=0.10.0",
        ],
    },
    keywords="audio, signal processing, waveshaping, distortion, effects, music",
    project_urls={
        "Bug Reports": "https://github.com/tsugumasa320/waveshaping-py/issues",
        "Source": "https://github.com/tsugumasa320/waveshaping-py",
        "Documentation": "https://github.com/tsugumasa320/waveshaping-py",
    },
)