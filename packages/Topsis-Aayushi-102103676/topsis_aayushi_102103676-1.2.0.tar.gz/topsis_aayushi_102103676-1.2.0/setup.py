# File: setup.py

import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Aayushi-102103676",  # Change this if you have a different name on PyPI
    version="1.2.0",  # Increment version for the new, fixed release
    description="A Python package to calculate TOPSIS scores and rank models.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AayushiPuri/topsis",  # Your GitHub URL
    author="Aayushi Puri",  # Your Name
    author_email="meaayushipuri@gmail.com",  # Your Email
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),  # This is better than hardcoding the name
    include_package_data=True,
    # CRITICAL: Add your package's dependencies here
    install_requires=["numpy", "pandas"],
    # This links the 'topsis' command to the main() function in your script
    entry_points={
        "console_scripts": [
            "topsis=TOPSIS.__main__:main",
        ]
    },
)