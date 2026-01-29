from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
setup(
    name="leetcode-terminal",  
    version="0.1.5",
    description="LeetCLI - Solve, practice, and fetch LeetCode challenges from your terminal",
    long_description = (this_directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Chitransh Saxena",
    author_email="geniussaxena007@gmail.com",
    url="https://github.com/Chitransh2309", 
    packages=find_packages(include=["*", "leet*"]),
    python_requires=">=3.7",
    install_requires=[
        "typer[all]>=0.9.0",
        "requests>=2.30.0",
        "rich>=13.0.0",
        "html2text",
    ],
    entry_points={
        "console_scripts": [
            "lc=leetcli.main:app", 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    include_package_data=True,
)
