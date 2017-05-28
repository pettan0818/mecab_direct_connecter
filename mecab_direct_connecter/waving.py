# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created: 日  5/28 23:55:39 2017

# Usage
#
"""
import pickle


def waving_words_filter(waving_dic_path: str, word_list: list):
    """filtering word_list by using check waving word dictionary.

    >>> waving_words_filter("./waving_dic.dic", ["お子様", "子供", "子ども"])
    ["子ども", "子ども", "子ども"]
    >>> waving_words_filter("./waving_dic.dic", ["テスト"])
    ['Test1']
    """
    waving_dic = load_dic_pickled_data(waving_dic_path)

    return [waving_dic.get(word, word) for word in word_list]


def load_dic_pickled_data(path: str):
    """reading dictionary data from path."""
    return pickle.load(open(path, "rb"))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
