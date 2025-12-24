"""
Setup script for NREL SLOPE Scraper
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="slopemap-scraper",
    version="1.0.0",
    author="Your Name",
    description="Multi-agent scraper for NREL SLOPE county energy data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aranyoray/SLOPEmap",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "slope-scrape=scraper.agent_scraper:main",
            "slope-parse=scraper.data_parser:main",
            "slope-dashboard=dashboard.app:main",
        ],
    },
)
