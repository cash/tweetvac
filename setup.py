#!/usr/bin/env python

from setuptools import setup

import tweetvac

setup(
    name='tweetvac',
    version=tweetvac.__version__,
    description='Package that makes sucking down tweets from Twitter easy.',
    long_description=open('README.rst').read(),
    author=tweetvac.__author__,
    author_email='cash.costello@gmail.com',
    url='https://github.com/cash/tweetvac',
    license=tweetvac.__license__,
    keywords='twitter tweet tweetvac cursor client',
    py_modules=['tweetvac'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'twython>=3.0'
    ]
)