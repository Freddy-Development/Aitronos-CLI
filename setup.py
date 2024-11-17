from setuptools import setup, find_packages
from setuptools import setup, find_packages

setup(
    name="aitronos",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here, if any
    entry_points={
        "console_scripts": [
            "aitronos=aitronos.cli:main",
        ],
    },
    author="Your Name",
    description="A CLI for Aitronos functionality",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aitronos",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)