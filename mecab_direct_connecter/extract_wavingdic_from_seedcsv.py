# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created: 日  5/21 17:37:11 2017

# Usage
#
"""
import codecs
import pickle
from functools import reduce
from operator import mul
from typing import Any
import fire


def def_file_reader(file_path: str):
    """表記揺れ辞書の作成

    >>> file_path = "./wikipedia_synonym.txt"
    """
    def def_file_validator(record_list):
        """表記揺れ辞書(代表表現, 代替表現, 代替表現, ...)"""
        record_len_checked_list = [len(i) for i in record_list]
        result_checker = reduce(mul, record_len_checked_list)

        if result_checker is False:
            raise TypeError("Read file is not valid to make dic.")

    record_list = []
    with codecs.open(file_path, "r", "utf-8") as con:
        for line in con.readlines():
            record_list.append([word.rstrip("\n") for word in line.split(",")])

    def_file_validator(record_list)

    return record_list


def waving_dic_maker(record_list: list):
    """Make a dictionary of waving expressions to representation_exp."""
    waving_dic = {}
    for record in record_list:
        representation_exp = record[0]
        for alt_exp in record[1:]:
            waving_dic.update({alt_exp: representation_exp})

    return waving_dic


def dumper(target_data: Any, output_pickle_name: str):
    """dumping target_data."""
    with open(output_pickle_name, 'w') as con:
        pickle.dump(target_data, con)


def main(input_path: str, output_pickle_name: str):
    """Fire Starter."""
    record_list_validated = def_file_reader(input_path)

    waving_dic = waving_dic_maker(record_list_validated)

    dumper(waving_dic, output_pickle_name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    fire.Fire(main)
