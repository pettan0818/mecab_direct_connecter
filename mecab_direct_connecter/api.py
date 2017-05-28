# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created: 日  5/28 14:50:28 2017

# Usage
#
"""
from collections import namedtuple
import logging

import neologdn
import MeCab

from morphing import MecabMother
from stopword import StopWordKiller

MECAB_LOGGER = logging.getLogger("api")
_STDOUT_HANDLER = logging.StreamHandler()
MECAB_LOGGER.addHandler(_STDOUT_HANDLER)
MECAB_LOGGER.setLevel(logging.DEBUG)

DEFAULT_DICT_PATH = [
    "-d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/lib64/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-x 未知語,*,*,*,*,*,*,*,* --eos-format="]
DEFAULT_STOPWORD_DIC = "./stopword.list"
DEFAULT_WAVING_DIC = "./waving.dic"


def setup(mecab_method=None, cleanup=None, normalization=None, stopword=None, waving=None):
    """setup mecab direct connecter.

    * Mecab parsing method.
    * word cleaning by mecab.
    * normalization processing.
    * stopword processing.
    * waving word processing.
    """
    setting = namedtuple("settings", ["mecab_method", "cleanup", "normalization", "stopword", "waving"])

    if mecab_method is None:
        setting.mecab_method = "original"
    else:
        setting.mecab_method = mecab_method

    if setting.mecab_method in ["original", "word"]:
        MECAB_LOGGER.warning("Plaese sepcify mecab parsing method by original or word, on this time setted up for original.")
        setting.mecab_method = "original"
    MECAB_LOGGER.info("mecab processing method: %s", mecab_method)

    if cleanup is None:
        setting.cleanup = True
    else:
        setting.cleanup = cleanup
    MECAB_LOGGER.info("cleanup of unknown word is: %s", setting.cleanup)

    if normalization is None:
        setting.normalization = True
    else:
        setting.normalization = normalization
    MECAB_LOGGER.info("normalization is: %s", setting.normalization)

    if stopword is None:
        setting.stopword = True
    else:
        setting.stopword = stopword
    MECAB_LOGGER.info("stopword filtering is: %s", setting.stopword)

    if waving is None:
        setting.waving = True
    else:
        setting.waving = waving
    MECAB_LOGGER.info("waving word filetering is: %s", setting.waving)

    return setting


def setup_path(mecab_dict_path=None, stopword_dic_path=None, waving_dic_path=None):
    """setup custom path of mecab processing.

    * mecab_dict_path
    * stopword_dic_path(str or list)
    DEFAULT IS ./stopword.list
    * waving_dic_path(str or list)
    DEFAULT IS ./waving.dic
    """
    def check_dict_availability(path) -> bool:
        """Check mecab dict positons is valid."""
        try:
            MeCab.Tagger(path)
        except RuntimeError:
            return False

        return True

    path_setting = namedtuple("path", ["mecab_arg", "stopword_dic", "waving_dic"])

    if mecab_dict_path:  # When mecab Path is given.
        mecab_arg = "-d {0} -x 未知語,*,*,*,*,*,*,*,* --eos-format=".format(mecab_dict_path)
        if not check_dict_availability(mecab_arg):
            path_setting.mecab_arg = mecab_arg
    else:  # path is not given.
        for mecab_arg in DEFAULT_DICT_PATH:  # Checking default dict path.
            if check_dict_availability(mecab_arg):
                path_setting.mecab_arg = mecab_arg
                break

            # raise RuntimeError("Mecab is not ready via DEFAULT_DICT_PATH and your given path, and FALLING BACK DICT")

    if stopword_dic_path:
        path_setting.stopword_dic = stopword_dic_path
    else:
        path_setting.stopword_dic = DEFAULT_STOPWORD_DIC

    if waving_dic_path:
        path_setting.waving_dic = waving_dic_path
    else:
        path_setting.waving_dic = DEFAULT_WAVING_DIC

    return path_setting


def morph(text: str, extract_parts=None, setting=None, path_setting=None):
    """Do Natural Language Analysis obeying setting tuple.

    # Setting up options on default.
    >>> morph("私はおなかが減っていますよ")
    ['は', 'おなか', '減る', 'て', 'いる', 'ます', 'よ']
    >>> setting = setup(mecab_method="original", cleanup=True, normalization=True, stopword=False, waving=False)
    >>> morph("私はおなかが減っていますよ", setting=setting)
    ['私', 'は', 'おなか', 'が', '減る', 'て', 'いる', 'ます', 'よ']
    >>> morph("私はおなかが減っていますよ", extract_parts="名詞", setting=setting)
    ['私', 'おなか']
    >>> setting = setup(mecab_method="word", cleanup=False, normalization=True, stopword=False, waving=False)
    >>> morph("私はおなかが減っていますよ", setting=setting)
    ['私', 'は', 'おなか', 'が', '減る', 'て', 'いる', 'ます', 'よ']
    """
    # argument parsing.
    if setting is None:
        MECAB_LOGGER.warning("please give me setting obj.")
        setting = setup()
    if path_setting is None:
        MECAB_LOGGER.warning("please give me setting path obj.")
        path_setting = setup_path()

    if isinstance(extract_parts, str):
        temp = []
        temp.append(extract_parts)
        extract_parts = temp

    mecab_parser = MecabMother(path_setting)

    if setting.normalization:
        text = neologdn.normalize(text)

    # Execute parse.
    mecab_parser.set_text_to_parse(text)

    if setting.cleanup:
        mecab_parser.unknown_word_buster_by_parts()
        mecab_parser.unknown_word_buster_by_readings()

    if setting.mecab_method == "original":
        result = mecab_parser.extract_category_originalshape(extract_parts)
    elif setting.mecab_method == "word":
        result = mecab_parser.extracted_category_word(extract_parts)

    if setting.stopword:
        killer = StopWordKiller(def_file=path_setting.stopword_dic)
        result = killer.killer(result)

    # if setting.waving:
    #     waving_word_killer

    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
