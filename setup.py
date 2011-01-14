#!/usr/bin/env python
try:
    from setuptools import setup
except:
    from distutils.core import setup


from setuptools import find_packages

setup(name='django-valuate',
      version='1.0-beta',
      description='A valuation system pluggable to any object',
      long_description=open('README').read(),
      author='Rohan Jain',
      author_email='dcrodjer@gmail.com',
      url='http://code.google.com/p/django-valuate/',
      packages=['valuate'],
      include_package_data=True,
      license="BSD",
      platforms=["all"],
      zip_safe = False
     )
