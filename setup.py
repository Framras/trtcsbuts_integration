# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

# get version from __version__ variable in trtcsbuts_integration/__init__.py
from trtcsbuts_integration import __version__ as version

setup(
    name='trtcsbuts_integration',
    version=version,
    description='TR Ministry of Health UTS integration of medical devices, etc for ErpNext',
    author='Framras AS-Izmir',
    author_email='bilgi@framras.com.tr',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
