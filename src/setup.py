# -*- coding: utf-8 -*-
"""
# install it by: pip install --process-dependency-links --trusted-host guthub.com -e .
"""

from os.path import join, dirname
import re
from setuptools import setup, find_packages
__author__ = 'vahid'

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'kakapo', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'wheezy.web',
    'argcomplete',
    'PyJWT',
    'simplejson'
    # 'khayyam',
    # 'itsdangerous',
]

setup(
    name="kakapo",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid@varzesh3.com",
    long_description=open(join('..', 'README.md'), encoding='UTF-8').read(),
    install_requires=dependencies,
    packages=find_packages(),
)
