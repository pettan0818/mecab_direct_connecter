# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from mecab_direct_connecter import __version__

setup(
    name="mecab_direct_connecter",
    version=__version__,
    description="Easily Mecab Wrapper",
    author="pettan0818",
    packages=find_packages(),
    install_requires=[
        "mecab-python3",
        "neologdn",
        "nltk",
    ]
)
