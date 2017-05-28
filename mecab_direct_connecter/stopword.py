# -*- coding: utf-8 -*-
"""Stop Word Remover.

This script is to remove stopwords from list.

Usage:
>>> tester = StopWordKiller()
>>> tester.killer(["あそこ", "ケーキ屋", "美味しい", "みたい"])
['ケーキ屋', '美味しい']
"""
import logging

MECAB_LOGGER = logging.getLogger("stopword")
_STDOUT_HANDLER = logging.StreamHandler()
MECAB_LOGGER.addHandler(_STDOUT_HANDLER)
MECAB_LOGGER.setLevel(logging.DEBUG)

PRE_DEFINED = ['あそこ', 'あたり', 'あちら', 'あっち', 'あと', 'あな', 'あなた', 'あれ', 'いくつ', 'いつ', 'いま', 'いや', 'いろいろ',
               'うち', 'おおまか', 'おまえ', 'おれ', 'がい', 'かく', 'かたち', 'かやの', 'から', 'がら', 'きた', 'くせ', 'ここ', 'こっち',
               'こと', 'ごと', 'こちら', 'ごっちゃ', 'これ', 'これら', 'ごろ', 'さまざま', 'さらい', 'さん', 'しかた', 'しよう', 'すか', 'ずつ',
               'すね', 'すべて', 'ぜんぶ', 'そう', 'そこ', 'そちら', 'そっち', 'そで', 'それ', 'それぞれ', 'それなり', 'たくさん', 'たち',
               'たび', 'ため', 'だめ', 'ちゃ', 'ちゃん', 'てん', 'とおり', 'とき', 'どこ', 'どこか', 'ところ', 'どちら', 'どっか', 'どっち',
               'どれ', 'なか', 'なかば', 'なに', 'など', 'なん', 'はじめ', 'はず', 'はるか', 'ひと', 'ひとつ', 'ふく', 'ぶり', 'べつ',
               'へん', 'ぺん', 'ほう', 'ほか', 'まさ', 'まし', 'まとも', 'まま', 'みたい', 'みつ', 'みなさん', 'みんな', 'もと', 'もの',
               'もん', 'やつ', 'よう', 'よそ', 'わけ', 'わたし', 'ハイ', '上', '中', '下', '字', '年', '月', '日', '時', '分', '秒',
               '週', '火', '水', '木', '金', '土', '国', '都', '道', '府', '県', '市', '区', '町', '村', '各', '第', '方', '何', '的',
               '度', '文', '者', '性', '体', '人', '他', '今', '部', '課', '係', '外', '類', '達', '気', '室', '口', '誰', '用', '界',
               '会', '首', '男', '女', '別', '話', '私', '屋', '店', '家', '場', '等', '見', '際', '観', '段', '略', '例', '系', '論',
               '形', '間', '地', '員', '線', '点', '書', '品', '力', '法', '感', '作', '元', '手', '数', '彼', '彼女', '子', '内',
               '楽', '喜', '怒', '哀', '輪', '頃', '化', '境', '俺', '奴', '高', '校', '婦', '伸', '紀', '誌', 'レ', '行', '列', '事',
               '士', '台', '集', '様', '所', '歴', '器', '名', '情', '連', '毎', '式', '簿', '回', '匹', '個', '席', '束', '歳', '目',
               '通', '面', '円', '玉', '枚', '前', '後', '左', '右', '次', '先', '春', '夏', '秋', '冬', '一', '二', '三', '四', '五',
               '六', '七', '八', '九', '十', '百', '千', '万', '億', '兆', '下記', '上記', '時間', '今回', '前回', '場合', '一つ',
               '年生', '自分', 'ヶ所', 'ヵ所', 'カ所', '箇所', 'ヶ月', 'ヵ月', 'カ月', '箇月', '名前', '本当', '確か', '時点', '全部',
               '関係', '近く', '方法', '我々', '違い', '多く', '扱い', '新た', 'その後', '半ば', '結局', '様々', '以前', '以後', '以降',
               '未満', '以上', '以下', '幾つ', '毎日', '自体', '向こう', '何人', '手段', '同じ', '感じ']

OFTEN_DEFINED = ["拝読", "の", "こと", "もの", "よう", "http://", "人", "私", "様", "ー", "一", "が", "ため", "方", "ほう", "こと", "場合",
                 "何", "さま", "それ", "これ", "ん", "相談者", "%", "さ", "mg", "少し", "WWW", "www", "html", "HTML", "お願い", "おねがい",
                 "よろしく", "申し訳", "まだ", "ミリ", "キロ", "センチ", "cm", "どう", "御返事", "ご自身", "位", "何日", "仮に", "まして",
                 "初め", "すぐ", "多分", "誠に", "お世話", "回答", "よい", "お気持ち", "宜しく", "やすい", "っぽい", "病", "症", "よく", "つまり",
                 "今日", "明日", "昨日", "よい", "師", "ヶ月前", "とても", "…。", "cc", "現在", "旨", "ふと", "大丈夫", "院", "付け", "先生", "半年",
                 "今年", "おそらく", "恐らく", ".jp", "情報", "科"]

ZENKAKU_NUM = ["１", "２", "３", "４", "５", "６", "７", "８", "９", "０"]
HANKAKU_NUM = list(range(0, 100))
ONE_LETTERS_UP = [chr(i) for i in range(65, 65 + 26)]
ONE_LETTERS_DOWN = [chr(i) for i in range(97, 97 + 26)]


def def_file_reader(def_file_pos):
    """Read stopword data which defines unneeded data per line.

    File should be represetnted as below.(No comma or spaces.)
    XXX
    YYY
    >>> def_file_reader("./tests/stopword.list")  # doctest: +SKIP
    [...]
    """
    if def_file_pos is None:
        return None
    try:
        with open(def_file_pos) as con:
            stopword_list = con.readlines()  # type: list

    except FileNotFoundError:
        MECAB_LOGGER.warning("def_file pos is invailed.")
        return None

    cleaned_stopword_list = [i.rstrip() for i in stopword_list]
    return [i for i in cleaned_stopword_list if not len(i) == 0]


class StopWordKiller(object):
    """Main Class of stopword removing."""
    def __init__(self, def_file=None, inline_def=None):
        additional_word = def_file_reader(def_file)

        temp = ZENKAKU_NUM + HANKAKU_NUM + ONE_LETTERS_UP + ONE_LETTERS_DOWN + OFTEN_DEFINED + PRE_DEFINED
        if inline_def is not None:
            temp += inline_def
        if additional_word is not None:
            temp += additional_word

        self.stop_word = list(set(temp))

    def set_more_stopwords(self, add_target: list):
        """Add Stopwords."""
        self.stop_word = self.stop_word.extend(add_target)

    def killer(self, list_data):
        """Kill Stop words from list.

        >>> stopworddisposal = StopWordKiller()
        >>> stopworddisposal.killer(["相談", "の", "相談者さま"])
        ['相談', '相談者さま']"""
        return [i for i in list_data if i not in self.stop_word]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
