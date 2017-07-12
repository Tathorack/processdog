#!/usr/bin/env python3
#coding=UTF-8

from setuptools import setup
from codecs import open

major_version = 0
minor_version = 0
build_version = 1

version = '{0}.{1}.{2}'.format(major_version, minor_version, build_version)

setup(name='processdog',
      version=version,
      description='Simple Subprocess Watchdog',
      long_description=open('README.rst', encoding='utf-8').read(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      keywords='Subprocess Timeout Watchdog',
      url='',
      author='Rhys Hansen',
      author_email='rhyshonline@gmail.com',
      license='MIT',
      packages=['processdog'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
