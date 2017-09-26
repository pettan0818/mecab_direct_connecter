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
    tokenizer = ToktokTokenizer().tokenize
    return tokenizer(text)


def english_normalizer(text: str):
    """英語表現の正規化

    * 以下の準備のための全ワードの小文字化処理
    * 語幹化
    * 見出し語化
    """
    pass


def stopword_filter(text: str):
    """英語表現用のstopwordフィルター

    NLTK付属のstopword Dictを利用する。
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
