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
    lang_info(lang=['J', 'E', 'J', 'E', 'J'], raw_text=['この車は、日本では', '4WD', 'と言われているが、その実態は', 'FD', 'である。'])
    >>> lang_distingisher("4WDはいいぞ。(https://ja.wikipedia.org/wiki/%E5%9B%9B%E8%BC%AA%E9%A7%86%E5%8B%95)")
    lang_info(lang=['E', 'J', 'E'], raw_text=['4WD', 'はいいぞ。', '(https://ja.wikipedia.org/wiki/%E5%9B%9B%E8%BC%AA%E9%A7%86%E5%8B%95)'])
    """
    lang_info = NamedTuple("lang_info", [("lang", list), ("raw_text", list)])

    # XXX: Naive way.
    # reuse for detecting lang.
    eng_finder = re.compile(r"[0-9A-Za-z_ :,./%()]+")
    # url_finder = re.compile(r"https?://[\w/:%#\$&\?~\.=\+\-]+")

    # Find english/URL text by matching re obj.
    eng_pos = re.finditer(eng_finder, text)
    # url_pos = re.finditer(url_finder, text)

    # Scheme
    # この問題の難しいところはsplitしてしまうと、英語部分が消えてしまうところにある
    # 1. 英語抜きの日本語だけのリストを作る
    # 2. 英語の場所を特定
    # 3. 1.で作ったリストに特定した部位にインサート
    # Find jpn text by spliting by English block.
    jpn_text = re.split(eng_finder, text)

    # 英語位置特定(injectパラメータ生成
    eng_text = []
    eng_start_pos = []
    for i in eng_pos:
        eng_text.append(i.group())
        eng_start_pos.append(i.start())

    # 英語をraw_textに反映する

def inject_eng_word(jpn_text: list, eng_start_pos: list, eng_text: list) -> list:
    """ this is tester wrap to inject func.
    >>> inject_eng_word(['この車は、日本では', 'と言われているが、その実態は', 'である。'], [9, 26], ['4WD', 'FD'])
    ['この車は、日本では', '4WD', 'と言われているが、その実態は', 'FD', 'である。']
    """
    def inject(latest_jpn_text: list, latest_eng_start_pos: list, latest_eng_text: list):
        """Actually inject word."""
        # Return if eng_text is empty.
        if not latest_eng_text:  # list which len is 0 => False
            return latest_jpn_text

        # must each time re-gen.
        jpn_text_len = [len(i) for i in latest_jpn_text]
        # make a list which contains splited summed chars.
        summed_jpn_text = sum_list_like_fibo(jpn_text_len)

        target_pos: int = latest_eng_start_pos.pop(0)
        target_eng_text: str = latest_eng_text.pop(0)
        inject_pos = summed_jpn_text.index(target_pos)

        latest_jpn_text.insert(inject_pos + 1, target_eng_text)

        # 再帰的にデータを更新
        return inject(latest_jpn_text, latest_eng_start_pos, latest_eng_text)

    return inject(jpn_text, eng_start_pos, eng_text)


def sum_list_like_fibo(target: list) -> list:
    """Sum list like fibo or as below.

    >>> sum_list_like_fibo([1, 2, 3, 4, 5])
    [1, 3, 6, 10, 15]
    >>> sum_list_like_fibo([9, 14, 4])
    [9, 23, 27]
    >>> sum_list_like_fibo([0, 5, 0])
    [0, 5, 5]
    >>> sum_list_like_fibo([0, 0, 0])
    [0, 0, 0]
    """
    return [sum(target[:i + 1]) for i in range(len(target))]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
