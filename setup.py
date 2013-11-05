''' Install sipcheck with setuptools '''

import os
from setuptools import setup

def read(fname):
    ''' Utility function to read the README file. '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='sipcheck',
      version='2.0.0',
      description='',
      url='https://github.com/sinologicnet/sipcheck',
      author='Elio Rojano, Sergio Cotelo, Javier Vidal',
      author_email='sipcheck@sinologic.net',
      license='GPL',
      scripts=['bin/sipcheck'],
      packages=['sipcheck'],
      package_dir={'sipcheck': 'sipcheck'},
      long_description=read('README.md'),
      zip_safe=False)
