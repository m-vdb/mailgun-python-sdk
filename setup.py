#!/usr/bin/env python

from setuptools import setup, find_packages


VERSION = '0.3'


setup(
    name='mailgun_sdk',
    version=VERSION,
    description='Mailgun Python SDK (unofficial)',
    author='Maxime Vdb',
    author_email='me@maxvdb.com',
    packages=find_packages(),
    install_requires=['requests', 'six'],
    license="MIT",
    keywords="mailgun_sdk api sdk",
    url='https://github.com/m-vdb/mailgun-python-sdk',
    download_url='https://github.com/m-vdb/mailgun-python-sdk/archive/v{}.tar.gz'.format(VERSION),
    project_urls={
        "Source Code": "https://github.com/m-vdb/mailgun-python-sdk",
    }
)
