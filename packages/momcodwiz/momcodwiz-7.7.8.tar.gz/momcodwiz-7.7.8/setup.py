from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="momcodwiz",
    version="7.7.8",
    packages=find_packages(),
    python_requires=">=3.8",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
