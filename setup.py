from os import path
from setuptools import find_packages, setup
here = path.abspath(path.dirname(__file__))

version_num = "1.0.0"

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='libinsult-client',
    version=version_num,
    description='A python client for the LibInsult insult generator web service',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Kevin Dious',
    author_email='kdious@yahoo.com',
    url='https://github.com/kdious/libinsult-client-python',
    download_url='https://github.com/kdious/libinsult-client-python/tarball/{ver}'.format(
        ver=version_num),
    install_requires=['future==1.0.0', 'requests'],
    packages=find_packages(),
    keywords=['libinsult', 'insult', 'generator', 'api', 'client'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
