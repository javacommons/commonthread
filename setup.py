# https://packaging.python.org/guides/making-a-pypi-friendly-readme/

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='commonthread',
    version='0.8',
    description='Common Threading Library',
    url='https://github.com/javacommons/commonthread',
    author='javacommons',
    author_email='javacommons@gmail.com',
    license='MIT',
    keywords='development',
    packages=[
        "commonthread",
    ],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
