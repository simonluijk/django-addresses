#!/usr/bin/env python
from distutils.core import setup

VERSION = __import__("addressbook").VERSION

setup(
    author="Simon Luijk",
    author_email="simon@simonluijk.com",
    name="django-addresses",
    version=VERSION,
    description="Some forms around a few models to manage addresses",
    url="https://github.com/simonluijk/django-addresses",
    packages=[
        "addressbook",
        "addressbook.conf",
        "addressbook.migrations",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
