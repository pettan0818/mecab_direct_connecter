# Mecab Connecter with useful NL pre-process.
[![Build Status](https://travis-ci.org/pettan0818/mecab_direct_connecter.svg?branch=api_rearrange)](https://travis-ci.org/pettan0818/mecab_direct_connecter)
# Purpose
This library is to call mecab lib with useful functions.

# Requirements
* python 3.6~
Variable type hinting.
* neologdn
* mecab (On system)
* mecab-python3
* pandas

# How to install
```shell
pip install git+https://github.com/pettan0818/mecab_direct_connecter.git
```

# EASY TUTORIAL
```python
from mecab_direct_connecter import api

# 最も簡単な操作方法
api.direct_morph("テキスト", "word", None)
stopword 有効
normalization 有効
waving 無効
cleaning 有効

第一引数(必須) ターゲットの文字列
第二引数(必須) 解析手法(単語をそのまま返すか、活用を戻してから返すか)
第三引数 抽出する品詞、なければNone、あれば、"名詞"など、ただし、複数品詞抽出する場合、リストで渡す。

この方法だと、stopwordの除去などが自動で有効化されてしまうので、いろいろ設定を変更したい場合めんどいです。

# 一般的な操作方法
setting_obj = api.setup(stopword=False)
有効無効を変更したい機能を指示するとそれを反映した設定オブジェクト(settings namedtuple)が返ってきます。
path_obj = api.setup_path(mecab_dict_path= "")

unit = api.MorphUnit(setting_obj, path_obj)
設定変更しない場合は、NoneでOK。
あとは、この設定を保持したunitでmorphすればOK.
unit.morph("テキスト", mode="original", extract_parts=None)
この状態で英語・日本語をパースして処理しています。
英語はnltkのtokenizer処理可能です。
```
