from setuptools import setup, find_packages

setup(
    name='aitronos',
    version='1.0.0',
    description='Aitronos CLI for various automation and project setup functionalities',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aitronos=aitronos.cli:main',
        ],
    },
    install_requires=[],
)