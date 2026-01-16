
from setuptools import setup, find_packages

with open('pypi_README.md', 'r') as f:
    description = f.read()

setup(
    name='gobrec',
    version='1.0.5',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy'
    ],
    long_description=description,
    long_description_content_type='text/markdown'
)