# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created: 木  8/31 06:42:32 2017

# Usage
#
"""
import re
from typing import NamedTuple


def lang_distingisher(text: str) -> NamedTuple:
    """determine text part lang and split.

    >>> lang_distingisher("この車は、日本では4WDと言われているが、その実態はFDである。")
    ["この車は、日本では", "4WD", "と言われているが、その実態は", "FD", "である。"]
    >>> lang_distingisher("4WDはいいぞ。(https://ja.wikipedia.org/wiki/%E5%9B%9B%E8%BC%AA%E9%A7%86%E5%8B%95)")
    ["4WD", "はいいぞ。", (https://ja.wikipedia.org/wiki/%E5%9B%9B%E8%BC%AA%E9%A7%86%E5%8B%95)"]
    """
    lang_info = NamedTuple("lang_info", [("lang", list), ("raw_text", list)])

    # XXX: Naive way.
    eng_finder = re.compile(r"[0-9A-Za-z_ :,./%()]+")
    # url_finder = re.compile(r"https?://[\w/:%#\$&\?~\.=\+\-]+")

    eng_pos = re.finditer(eng_finder, text)
    # url_pos = re.finditer(url_finder, text)

    url_pos = re.finditer(url_filter, text)

    for i in eng_pos:
        print(i.group())
        print(i.end() - i.start())

    for i in url_pos:
        print(i.group())
        print(i.end() - i.start())

    # return lang_info(lang, raw_text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
