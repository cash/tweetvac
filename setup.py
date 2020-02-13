from setuptools import setup

__author__ = 'Cash Costello'
__version__ = '1.0'

setup(
    name='tweetvac',
    version=__version__,
    description='Package that makes sucking down tweets from Twitter easy.',
    long_description=open('README.rst').read(),
    author=__author__,
    author_email='cash.costello@gmail.com',
    url='https://github.com/cash/tweetvac',
    license='MIT',
    keywords='twitter tweet tweetvac cursor client',
    py_modules=['tweetvac'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'twython>=3.0.0'
    ]
)
