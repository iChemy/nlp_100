from pprint import pprint
from collections.abc import Iterable
import random


def reverse_00():
    """
    https://nlp100.github.io/ja/ch01.html#00-文字列の逆順
    """
    s = "stressed"
    print(s[::-1])  # ストライド


def idx_01():
    """
    https://nlp100.github.io/ja/ch01.html#01-パタトクカシーー
    """
    s = "パタトクカシーー"
    print(s[0:7:2])


def alt_concat_02():
    """
    https://nlp100.github.io/ja/ch01.html#02-パトカータクシーパタトクカシーー
    """
    s1 = "パトカー"
    s2 = "タクシー"

    ret = ""
    for c1, c2 in zip(s1, s2):
        ret += c1 + c2

    print(ret)


def split_03():
    """
    https://nlp100.github.io/ja/ch01.html#03-円周率
    """
    s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
    word_list = s.split(" ")
    for i in range(0, len(word_list)):
        word_list[i] = word_list[i].rstrip(",.")  # 単語の末尾部分を除去

    ret = [len(w) for w in word_list]
    print(ret)


def dict_04():
    """
    https://nlp100.github.io/ja/ch01.html#04-元素記号
    """
    s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    word_list = s.split(" ")
    idxs = [0, 4, 5, 6, 7, 8, 14, 15, 18]

    ret = {}
    for i, w in enumerate(word_list):
        if i in idxs:
            ret[i + 1] = w[0:1]
        else:
            ret[i + 1] = w[0:2]
    pprint(ret)


def n_gram(iterable: Iterable, n) -> list[any]:
    ret = []
    for i in range(0, len(iterable) - n + 1, 1):
        ret.append(iterable[i : i + n])
    return ret


def bigram_05():
    """
    https://nlp100.github.io/ja/ch01.html#05-n-gram
    """
    s = "I am an NLPer"
    word_list = s.split(" ")

    # 文字bi-gram
    char_bigrams = n_gram(s, 2)
    # 単語bi-gram
    word_bigrams = n_gram(word_list, 2)

    print(char_bigrams)
    print(word_bigrams)


def gram_set_06():
    """
    https://nlp100.github.io/ja/ch01.html#06-集合
    """
    s1 = "paraparaparadise"
    s2 = "paragraph"
    X = set(n_gram(s1, 2))
    Y = set(n_gram(s2, 2))

    XY_union = X.union(Y)
    print("union")
    print(XY_union)

    XY_cross = X.intersection(Y)
    print("cross")
    print(XY_cross)

    XY_diff = X.difference(Y)
    print("diff")
    print(XY_diff)

    print(f'"se" in X: {"se" in X}')
    print(f'"se" in Y: {"se" in Y}')


def str_template(x, y, z) -> str:
    return str.format("{}時の{}は{}", x, y, z)


def format_07():
    """
    https://nlp100.github.io/ja/ch01.html#07-テンプレートによる文生成
    """
    print(
        'str_template(x=12, y="気温", z=22.4) -> '
        + str_template(x=12, y="気温", z=22.4)
    )


def ciper(text: str) -> str:
    ret = ""
    for c in text:
        if c.islower():
            ret += chr(219 - ord(c))
        else:
            ret += c
    return ret


def crypto_08():
    """
    https://nlp100.github.io/ja/ch01.html#08-暗号文
    """
    print('ciper("Hello, World!!") -> ' + ciper("Hello, World!!"))
    print('ciper(ciper("Hello, World!!")) -> ' + ciper(ciper("Hello, World!!")))


def g(word: str) -> str:
    """
    単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替える．
    ただし，長さが４以下の単語は並び替えない．
    """
    if len(word) <= 4:
        return word

    ret = word[0]
    ret += "".join(random.sample(word[1:-1], len(word[1:-1])))
    ret += word[-1]
    return ret


def typo_09():
    """
    https://nlp100.github.io/ja/ch01.html#09-typoglycemia
    """
    s = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    word_list = s.split(" ")

    print(" ".join([g(w) for w in word_list]))


if __name__ == "__main__":
    reverse_00()
    idx_01()
    alt_concat_02()
    split_03()
    dict_04()
    bigram_05()
    gram_set_06()
    format_07()
    crypto_08()
    typo_09()
