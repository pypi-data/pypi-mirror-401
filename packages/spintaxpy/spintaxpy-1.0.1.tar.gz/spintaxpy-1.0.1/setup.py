"""Setup configuration for spintaxpy library."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spintaxpy",
    version="1.0.1",
    author="alwahib",
    description="A combinatorial string generation library that creates all possible combinations from templates with variable elements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alwahib/spintax-py",
    project_urls={
        "Bug Tracker": "https://github.com/alwahib/spintax-py/issues",
        "Source Code": "https://github.com/alwahib/spintax-py",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    keywords=["spintax", "text generation", "combinatorial", "string variation", "template", "pattern"],
    python_requires='>=3.6',
    include_package_data=True,
)
