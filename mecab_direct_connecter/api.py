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
import logging
from collections import namedtuple
from pprint import pprint

import MeCab

import neologdn

try:  # library scenario, __init__ will import requried libs.
    TEMP_TESTER = MecabMother()  # ASAP GC
    del TEMP_TESTER
except NameError:  # for importing test or lib folder scenario.
    from morphing import MecabMother
    from stopword import StopWordKiller
    from waving import waving_words_filter


MECAB_LOGGER = logging.getLogger("api")
_STDOUT_HANDLER = logging.StreamHandler()
MECAB_LOGGER.addHandler(_STDOUT_HANDLER)
MECAB_LOGGER.setLevel(logging.WARNING)

DEFAULT_DICT_PATH = [
    "-d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/lib64/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-d /usr/lib/mecab/dic/mecab-ipadic-neologd -x 未知語,*,*,*,*,*,*,*,* --eos-format=",
    "-x 未知語,*,*,*,*,*,*,*,* --eos-format="]
DEFAULT_STOPWORD_DIC = "./stopword.list"
DEFAULT_WAVING_DIC = "./waving.dic"


def setup(cleanup=None, normalization=None, stopword=None, waving=None):
    """setup mecab direct connecter.

    * word cleaning by mecab.
    * normalization processing.
    * stopword processing.
    * waving word processing.
    """
    setting = namedtuple(
        "settings", ["cleanup", "normalization", "stopword", "waving"])

    if cleanup is None:
        cleanup = True
    else:
        cleanup = cleanup
    MECAB_LOGGER.info("cleanup of unknown word is: %s", cleanup)

    if normalization is None:
        normalization = True
    else:
        normalization = normalization
    MECAB_LOGGER.info("normalization is: %s", normalization)

    if stopword is None:
        stopword = True
    else:
        stopword = stopword
    MECAB_LOGGER.info("stopword filtering is: %s", stopword)

    if waving is None:
        waving = False
    else:
        waving = waving
    MECAB_LOGGER.info("waving word filetering is: %s", waving)

    return setting(cleanup, normalization, stopword, waving)


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

    path_setting = namedtuple(
        "path", ["mecab_arg", "stopword_dic", "waving_dic"])

    if mecab_dict_path:  # When mecab Path is given.
        mecab_arg = "-d {0} -x 未知語,*,*,*,*,*,*,*,* --eos-format=".format(
            mecab_dict_path)
        if not check_dict_availability(mecab_arg):
            mecab_arg = mecab_arg
    else:  # path is not given.
        for mecab_arg in DEFAULT_DICT_PATH:  # Checking default dict path.
            if check_dict_availability(mecab_arg):
                mecab_arg = mecab_arg
                break

    if stopword_dic_path:
        stopword_dic = stopword_dic_path
    else:
        stopword_dic = DEFAULT_STOPWORD_DIC

    if waving_dic_path:
        waving_dic = waving_dic_path
    else:
        waving_dic = DEFAULT_WAVING_DIC

    return path_setting(mecab_arg, stopword_dic, waving_dic)


def morph(text: str, mode=None, extract_parts=None, setting=None, path_setting=None):
    """Do Natural Language Analysis obeying setting tuple.This is high class def.

    # Setting up options on default.
    >>> setting = setup(waving=False)
    >>> morph("私はおなかが減っていますよ", mode="original",  path_setting=None, setting=setting)
    ['は', 'おなか', '減る', 'て', 'いる', 'ます', 'よ']
    >>> setting = setup(cleanup=True, normalization=True, stopword=False, waving=False)
    >>> morph("私はおなかが減っていますよ", mode="original", setting=setting)
    ['私', 'は', 'おなか', 'が', '減る', 'て', 'いる', 'ます', 'よ']
    >>> morph("私はおなかが減っていますよ", mode="original",  extract_parts="名詞", setting=setting)
    ['私', 'おなか']
    >>> setting = setup(cleanup=False, normalization=True, stopword=False, waving=False)
    >>> morph("私はおなかが減っていますよ", mode="original", setting=setting)
    ['私', 'は', 'おなか', 'が', '減る', 'て', 'いる', 'ます', 'よ']
    """
    # argument parsing.
    if setting is None:
        MECAB_LOGGER.debug("[api] no given setup obj, use default.")
        setting = setup()
    if path_setting is None:
        MECAB_LOGGER.debug("[api] no given setup path obj, use default.")
        path_setting = setup_path()

    if mode not in ["original", "word"]:
        raise NameError("Plaese specify mode as original or word.")

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

    if mode == "original":
        result = mecab_parser.extract_category_originalshape(extract_parts)
    elif mode == "word":
        result = mecab_parser.extracted_category_word(extract_parts)

    if setting.stopword:
        killer = StopWordKiller(def_file=path_setting.stopword_dic)
        result = killer.killer(result)

    if setting.waving:
        result = waving_words_filter(path_setting.waving_dic, result)

    return result


class MopheUnit():
    """

    # DEFAULT_USAGE
    >>> unit = MopheUnit()
    """

    def __init__(self, setup_obj=None, setup_path_obj=None):
        """initialize mopher unit.

        * setup objects are stored in property.
        """
        self.setup_obj = setup_obj
        self.path_obj = setup_path_obj

        if self.setup_obj is None:
            self.setup_obj = setup()
        if self.path_obj is None:
            self.path_obj = setup_path()

        if MECAB_LOGGER.level == logging.DEBUG:
            self.check_setting()

    def check_setting(self):
        """Check this instance setting.
        >>> unit = MopheUnit()
        >>> unit.check_setting() # doctest: +ELLIPSIS
        settings(...)
        path(...)
        """
        pprint(self.setup_obj)
        pprint(self.path_obj)

    def morph(self, text: str):
        """set morph text.

        >>> unit = MopheUnit()
        >>> unit.morph("テストです")
        """
        pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
