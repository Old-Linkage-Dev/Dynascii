#!/usr/bin/env python
#-*- coding:utf-8 -*-

import setuptools;
import dynascii;


_description = (
    "Dynascii is a light-weighted utility or application to casting things "
    "to a stream. It is implemented in Python and aimed to deploy quickly and "
    "easily on a server with a proper environment."
);

with open("README.md", "r", encoding="utf-8") as f_readme:
    _long_description = f_readme.read();


setuptools.setup(
    name = "dynascii",
    packages = [
        "dynascii",
        "dynascii.shell",
        "dynascii.shell.contrib"
    ],
    author = dynascii.__author__,
    author_email = "dont@email.me",
    version = dynascii.__version__.split()[1],
    license = dynascii.__license__,
    python_requires = ">=3.7, <4",
    description = _description,
    long_description = _long_description,
    long_description_content_type = "text/markdown",
    url = dynascii.__url__,
    project_urls = {
        "Bug Reports": dynascii.__url__ + "/issues",
        "Source": dynascii.__url__,
    },
    keywords = [
        "Dynascii",
        "ASCII",
        "ASCII Art",
        "TELNET",
        "Tarcadia"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    
);