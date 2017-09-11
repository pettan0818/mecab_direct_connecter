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
from nltk.tokenize import \
    ToktokTokenizer  # faster and more accuracy tokenizer.


def english_tokenzier(text: str):
    """return english tokenized list.

    >>> english_tokenzier("Hello World")
    ['Hello', 'World']
    >>> english_tokenzier("Keyboard Shortcuts Keyboard shortcuts are available for common actions and site navigation.")
    ['Keyboard', 'Shortcuts', 'Keyboard', 'shortcuts', 'are', 'available', 'for', 'common', 'actions', 'and', 'site', 'navigation', '.']
    """
    TOKENIZER = ToktokTokenizer().tokenize
    return TOKENIZER(text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
