# -*- coding: utf-8 -*-

from setuptools import setup
from mecab_direct_connecter import __version__

setup(
    name="mecab_direct_connecter",
    version=__version__,
    description="Easily Mecab Wrapper",
    author="pettan0818",
    packages=["mecab_direct_connecter"],
    install_requires=[
        "mecab-python3",
        "neologdn",
        "pandas"
    ],
    package_data={"mecab_direct_connecter": ["mecab_direct_connecter/stop_words.data"]}
)
