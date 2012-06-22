# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
import re
from os import path

v_file = open(path.join(path.dirname(__file__), 
                        'ceda_markup', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(v_file.read()).group(1)

setup(
    name='ceda-markup',
    version=VERSION,
    author=u'Maurizio Nagni',
    author_email='maurizio.nagni',
    packages=find_packages(),
    url='http://proj.badc.rl.ac.uk/svn/ndg/mauRepo/CedaMarkup',
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