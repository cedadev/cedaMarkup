# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='ceda_markup',
    version='0.0.1',
    author=u'Maurizio Nagni',
    author_email='maurizio.nagni',
    packages=find_packages(),
    url='http://ciprod1.cems.rl.ac.uk/pip/ceda_markup',
    license='BSD licence, see LICENCE',
    description='Collection of markup classes as geosrss, gml, atom, rss...' + \
                ' Contains an OpenSearch server (just the core not the server)',
    long_description=open('README').read(),
    zip_safe=False,
)

'''
zip_safe=False option. It prevents the package manager to install a 
      python egg, instead you'll get a real directory with files in it.
'''