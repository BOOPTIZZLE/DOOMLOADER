from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="doomloader",
    version="1.0.0",
    author="DOOMLOADER Team",
    author_email="doomloader@example.com",
    description="A tool for loading and processing NAM files for amp simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BOOPTIZZLE/DOOMLOADER",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Musicians",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "doomloader=doomloader.cli:main",
        ],
    },
    include_package_data=True,
    keywords="audio, amp simulation, NAM, neural amp modeler, guitar, effects",
)