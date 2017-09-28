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
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
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


def english_normalizer(tokenized_text: str, stopword_filter: bool=True):
    """英語表現の正規化

    * 以下の準備のための全ワードの小文字化処理
    * 語幹化
    * 見出し語化
    """
    # 正規化(語幹化・見出し語化)の準備のための小文字化
    target_text = [word.lower() for word in tokenized_text]

    # 語幹化(活用の排除) stemmer

    # 見出し語化(sとかingとか状況によって取り去る) lemmatize
    return None


def stopword_filter(tokenized_text: list):
    """英語表現用のstopwordフィルター

    NLTK付属のstopword Dictを利用する。
    >>> stopword_filter(["This", "is", "special", "apple", "."])
    ['special', 'apple', '.']
    """
    stopword_set = set(stopwords.words("english"))

    target_text = [word.lower() for word in tokenized_text]

    return [word for word in target_text if word not in stopword_set]


def pos_filtering(tokenized_text: list, filter_pos: list):
    """品詞フィルター powered by TreeTagger

    TreeTaggerをsubprocessか何かで呼んで、品詞情報を取得。
    品質情報によるフィルターを提供する。
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
