import os
import sys
import spacy
import pandas as pd
from functools import reduce
import collections
import matplotlib.pyplot as plt
import seaborn as sns
# from pprint import pprint

# https://qiita.com/derodero24/items/b49dd92e14c7e7655ccc を参考にしている


def get_text():
    if os.system("curl https://nlp100.github.io/data/neko.txt -o  src/neko.txt") != 0:
        sys.exit()


def morpho_analysis():
    nlp = spacy.load("ja_ginza_electra")
    with open("src/neko.txt") as f1, open("src/neko.txt.ginza", "w") as f2:
        for line in f1:
            for sent in nlp(line.strip()).sents:
                for token in sent:
                    if token.is_sent_end:
                        continue  # <- EOS だけの行が出てきて処理が大変なので...
                    # i:トークン番号, orth_:表層形, lemma_:基本形,
                    # pos_:品詞（英語）, tag_:きめ細かな品詞。 <- spacy の tag_ の説明
                    f2.write(
                        f"{token.i}\t{token.orth_}\t{token.lemma_}\t"
                        f"{token.pos_}\t{token.tag_}\n"
                    )
                # f2.write("EOS\n")


def morfo_dict_list_30() -> list[list[dict]]:
    """
    ```
    {
        "surface": 表層形,
        "base": 基本形,
        "pos": 品詞名,
        "pos1": きめ細かな品詞
    }
    ``
    """
    df = pd.read_csv("src/neko.txt.ginza", header=None, delimiter="\t")
    ret: list[list[dict]] = []
    sent: list[dict] = []
    for _, row in df.iterrows():
        pos, *pos1 = str(row[4]).split("-")  # リストの先頭は pos に残りは pos1 に
        neko_dict = {"surface": row[1], "base": row[2], "pos": pos, "pos1": pos1}
        sent.append(neko_dict)
        if row[2] == "。":
            ret.append(sent)
            sent = []

    if len(sent) != 0:
        ret.append(sent)
        sent = []

    return ret


def get_surfaces_31() -> list[str]:
    mor_dicts = morfo_dict_list_30()
    ret = []
    for sentence in mor_dicts:
        for morpheme in sentence:
            ret.append(morpheme["surface"])

    return ret


def get_base_32() -> list[str]:
    mor_dicts = morfo_dict_list_30()
    ret = []
    for sentence in mor_dicts:
        for morpheme in sentence:
            ret.append(morpheme["base"])

    return ret


def get_no_maishiku_33() -> list[str]:
    mor_dicts = morfo_dict_list_30()
    ret = []
    for sentence in mor_dicts:
        for i in range(len(sentence) - 2):
            if (
                sentence[i]["pos"] == "名詞"
                and sentence[i + 1]["surface"] == "の"
                and sentence[i + 2]["pos"] == "名詞"
            ):
                ret.append(
                    sentence[i]["surface"]
                    + sentence[i + 1]["surface"]
                    + sentence[i + 2]["surface"]
                )
    print(ret)
    return ret


def get_long_meishi(sent_dict: list[dict]) -> list[str]:
    i = 0
    sent_mor_num = len(sent_dict)
    count = 0
    buf: str = ""
    ret: list[str] = []

    while i < sent_mor_num:
        if sent_dict[i]["pos"] != "名詞":
            if count >= 2:
                ret.append(buf)
            buf = ""
            count = 0
            i += 1
            continue
        count += 1
        buf += sent_dict[i]["surface"]
        i += 1

    return ret


def get_renzoku_maishi_34() -> list[str]:
    mor_dicts = morfo_dict_list_30()
    ret: list[str] = []
    for sentence in mor_dicts:
        meishis = get_long_meishi(sentence)
        ret += meishis
    return ret


def freq_anly_35() -> list[tuple[str, int]]:
    mor_dicts = morfo_dict_list_30()
    # 二次元リストをflatten
    words = reduce(list.__add__, mor_dicts)
    # 単語だけを抜き出し
    words = collections.Counter(map(lambda e: e["surface"], words))
    # 出現頻度を算出
    ret: list[tuple[str, int]] = words.most_common()
    # 出現頻度順にソート
    ret = sorted(ret, key=lambda e: e[1], reverse=True)

    return ret


def get_freq_hist_36():
    words = freq_anly_35()
    words_df = pd.DataFrame(words[:10], columns=["word", "count"])
    sns.set_theme(font="AppleMyungjo")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(words_df["word"], words_df["count"])
    plt.show()


def get_neko_coll(sent: list[dict]) -> list[str]:
    idxs: set[int] = set([])
    for i, morp in enumerate(sent):
        if morp["surface"] == "猫":  # base の方が良い説
            if i - 1 >= 0:
                idxs.add(i - 1)
            if i + 1 < len(sent):
                idxs.add(i + 1)
    ret = []
    for i in idxs:
        ret.append(sent[i]["surface"])  # base の方が良い説

    return ret


def get_coll_neko_37():
    mor_dicts = morfo_dict_list_30()
    ret: list[str] = []
    for sent in mor_dicts:
        colls_in_sent = get_neko_coll(sent)
        ret += colls_in_sent

    cats = collections.Counter(ret)
    # 出現頻度を算出
    cats = cats.most_common()
    # 出現頻度順にソート
    cats = sorted(cats, key=lambda e: e[1], reverse=True)

    cats_df = pd.DataFrame(cats[:10], columns=["word", "count"])
    sns.set_theme(font="AppleMyungjo")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(cats_df["word"], cats_df["count"])
    plt.show()


def freq_word_count_hist_38():
    words = freq_anly_35()
    hist_df = pd.DataFrame(words, columns=["word", "count"])
    sns.set_theme(font="AppleMyungjo")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(hist_df["count"], range=(1, 100))
    plt.show()


def zipf_39():
    words = freq_anly_35()
    zipf_df = pd.DataFrame(words, columns=["word", "count"])
    sns.set_theme(font="AppleMyungjo")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.plot(zipf_df["count"])
    plt.show()


if __name__ == "__main__":
    get_text()
    morpho_analysis()
    zipf_39()
