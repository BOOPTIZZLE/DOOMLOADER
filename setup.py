from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="doomloader",
    version="0.1.0-alpha",
    author="BOOPTIZZLE",
    description="A Python-based audio file loader and processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BOOPTIZZLE/DOOMLOADER",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core dependencies will be added as the project develops
        # "numpy>=1.20.0",
        # "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "doomloader=doomloader.cli:main",
        ],
    },
)