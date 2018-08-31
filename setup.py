#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup
from setuptools.command.test import test as TestCommand


for line in open('playrix/__init__.py'):
    match = re.match("__version__ *= *'(.*)'", line)
    if match:
        __version__, = match.groups()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        raise SystemExit(errno)


setup(
    name='playrix',
    version=__version__,
    description='Playrix test task',
    url='https://github.com/devforfu/playrix',
    packages=['playrix'],
    install_requires=[
      'click>=6.7',
      'numpy==1.15.1',
      'pandas==0.23.4'
    ],
    test_require=['pytest'],
    cmdclass={'test': PyTest}
)
