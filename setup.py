#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(name='django-valuate',
      version='0.5',
      description='A valuation system pluggable to any object',
      long_description=open('README').read(),
      author='Rohan Jain',
      author_email='m@rohanjain.in',
      url='http://code.google.com/p/django-valuate/',
      packages=['valuate', 'valuate.templatetags'],
      include_package_data=True,
      license="BSD",
      platforms=["all"],
     )
