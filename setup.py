#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mailgun-python-sdk',
    version='0.1',
    description='Mailgun Python SDK (unofficial)',
    author='Maxime Vdb',
    author_email='me@maxvdb.com',
    packages=find_packages(),
    install_requires=['requests'],
    license="MIT",
    keywords="mailgun api sdk",
    project_urls={
        "Source Code": "https://github.com/m-vdb/mailgun-python-sdk",
    }
)
