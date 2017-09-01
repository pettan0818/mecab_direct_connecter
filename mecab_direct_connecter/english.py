# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created: 木  8/31 06:42:06 2017

# Usage
#
"""
from nltk.tokenize import ToktokTokenizer

tokenizer = ToktokTokenizer().tokenize


def english_tokenzier(text: str):
    """return english tokenized list."""
    return tokenizer(text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
