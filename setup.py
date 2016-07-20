#!python3
import sys
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    README = f.read()

requirements = []
if sys.version_info < (3, 4):
    requirements.append('enum34')

setup(
    name='cue_sdk',
    version='2.1.0',

    description='Python wrapper for the CUE SDK',
    long_description=README,

    author='10se1ucgo',
    author_email='the10se1ucgo@gmail.com',

    license='Apache License, Version 2.0',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: System :: Hardware',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='Corsair CUE Strafe Void Scimitar K95 K70 K65 M65 Sabre RGB Keyboard Mouse',

    packages=['cue_sdk'],

    install_requires=requirements
)
