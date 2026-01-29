from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Gurdarshan-102303217",
    version="1.0.2",
    author="Gurdarshan Singh",
    author_email="gsingh6_be23@thapar.edu",
    description="A Python package for TOPSIS method for MCDM problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "topsis=102303217.102303217:main",
        ],
    },
)