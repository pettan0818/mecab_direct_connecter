# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "mecab_direct_connector",
    version = "0.0.1",
    description="Easily Mecab Wrapper",
    author = "pettan0818",
    packages = find_packages(),
    install_requires = [
        "mecab-python3",
        "neologdn",
        "pandas"
    ]
)