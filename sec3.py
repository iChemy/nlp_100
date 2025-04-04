import json
import os
import sys
import regex
from pprint import pprint
import requests


def get_file():
    if (
        (
            os.system(
                "curl https://nlp100.github.io/data/jawiki-country.json.gz -o src/jawiki-country.json.gz --create-dirs"
            )
            != 0
        )
        and (os.system("gunzip -d src/jawiki-country.json.gz")) != 0
        and (os.system("rm src/jawiki-country.json.gz")) != 0
    ):
        sys.exit(1)


def get_british_json_text() -> str:
    f = open("src/jawiki-country.json", "r", encoding="utf-8")
    jsons = f.readlines()
    f.close()

    text: str

    for j in jsons:
        data = json.loads(j)
        if data["title"] == "イギリス":
            text = data["text"]
            break

    return text


def get_json_20():
    """
    https://nlp100.github.io/ja/ch03.html#20-jsonデータの読み込み
    """
    get_file()
    print(get_british_json_text())


def get_category_lines_21():
    """
    https://nlp100.github.io/ja/ch03.html#21-カテゴリ名を含む行を抽出
    """
    text = get_british_json_text()
    lines = text.splitlines()

    # 行を抽出せよとのことなので 行頭 行末 マッチにしている
    # wikipedia の早見表 を見る限り行頭以外でも Category 宣言は使えそうなので注意
    category_pattern = regex.compile(r"^\[\[Category\:(?P<cat_name>[^\[\]]+)\]\]$")
    categories = list(
        filter(lambda line: regex.match(category_pattern, line) is not None, lines)
    )

    pprint(categories)


def get_categories_22():
    """
    https://nlp100.github.io/ja/ch03.html#22-カテゴリ名の抽出
    """
    text = get_british_json_text()
    lines = text.splitlines()

    # 行を抽出せよとのことなので 行頭 行末 マッチにしている
    # wikipedia の早見表 を見る限り行頭以外でも Category 宣言は使えそうなので注意
    category_pattern = regex.compile(r"^\[\[Category\:(?P<cat_name>[^\[\]]+)\]\]$")
    category_names = list(
        map(
            lambda match_ret: match_ret.group("cat_name"),
            filter(
                lambda match_ret_or_none: match_ret_or_none is not None,
                map(lambda line: regex.match(category_pattern, line), lines),
            ),
        )
    )

    pprint(category_names)


def get_section_and_type_23():
    """
    https://nlp100.github.io/ja/ch03.html#23-セクション構造
    """
    text = get_british_json_text()
    lines = text.splitlines()

    # 行のはじめに入力した場合のみ有効となるもの に該当するので行頭マッチ
    sec_ptrn = regex.compile(r"^(?P<sec_kind>={2,6})(?P<sec_name>.+)\1")

    ret = []
    for line in lines:
        match_ret = regex.match(sec_ptrn, line)
        if match_ret is None:
            continue
        sec_kind = len(match_ret.group("sec_kind")) - 1
        sec_name = match_ret.group("sec_name")
        ret.append((sec_kind, sec_name))

    pprint(ret)


def get_media_file_ref_24():
    """
    https://nlp100.github.io/ja/ch03.html#24-ファイル参照の抽出
    """
    text = get_british_json_text()
    lines = text.splitlines()

    media_ptrn = regex.compile(r"\[\[ファイル:(?P<media_name>[^|]+)\|\s*thumb\s*\|")
    ret = []
    for line in lines:
        match_ret_list: list[str] = regex.findall(media_ptrn, line)
        if len(match_ret_list) == 0:
            continue
        ret += [
            "ファイル:" + match_ret.replace(" ", "_") for match_ret in match_ret_list
        ]

    pprint(ret)


def extract_template_25() -> dict[str, str]:
    """
    https://nlp100.github.io/ja/ch03.html#25-テンプレートの抽出
    """
    text = get_british_json_text()
    # テンプレートは {{}} で囲まれている．
    # ただし テンプレートの内部 (content) でも {{}} が使われる可能性があるので入れ子で取得する必要がある
    double_flag_ptrn = regex.compile(
        r"(?P<template>\{\{(?P<content>(?:(?&template)|[^{}])+)\}\})",  # テンプレートを取得する regex
        flags=regex.MULTILINE | regex.DOTALL,
    )

    templates = regex.findall(double_flag_ptrn, text)

    # 基礎情報テンプレートに該当するパターン
    basic_info_ptrn = regex.compile(
        r"^\{\{基礎情報 国(?P<values>.+)\}\}$",
        flags=regex.MULTILINE | regex.DOTALL,
    )

    for template in templates:
        match_ret = regex.match(basic_info_ptrn, template[0])
        if regex.match(basic_info_ptrn, template[0]):
            basic_info_content = match_ret.group("values")

    # テンプレートにはいろんな使われ方があるが
    # {{テンプレート名|テンプレート変数1=引数1|テンプレート変数2=引数2|.....}}
    # 今回はこれ
    # 引数部分には 他のテンプレート {{}} や [[]] が入ってくるためそれをうまく
    # 避ける必要がある
    # 今回は
    # テンプレート名|テンプレート変数1=引数1|テンプレート変数2=引数2|.....
    # の部分を取り出せているので...
    key_value_pair_ptrn = regex.compile(
        r"\|"
        r"(?P<key>[^=]+?)"
        r"\s*"
        r"\=\s*"
        r"(?P<value>(?:"
        r"[^{}\[\]|]+"
        r"|"
        r"(?P<template>\{\{(?:(?&template)|[^{}])+\}\})"
        r"|"
        r"(?P<file_or_cat>\[\[[^\[\]]+\]\])"
        r")+)",
        flags=regex.MULTILINE | regex.DOTALL,
    )
    ret_dict: dict[str, str] = {}
    match_rets = regex.findall(key_value_pair_ptrn, basic_info_content)
    for match_ret in match_rets:
        ret_dict[match_ret[0]] = match_ret[1]

    # pprint(ret_dict)

    return ret_dict


def remove_emp(text: str) -> dict[str, str]:
    # count を指定してないので全部置換してくれる
    new = regex.sub(r"('{2,5})(.*?)\1", r"\2", text)
    return new


def remove_emp_26() -> dict[str, str]:
    """
    https://nlp100.github.io/ja/ch03.html#26-強調マークアップの除去
    """
    temp_dict = extract_template_25()
    for k, v in temp_dict.items():
        temp_dict[k] = remove_emp(v)

    # pprint(temp_dict)
    return temp_dict


def remove_inner_link(text: str) -> str:
    """
    [[記事名]] -> 記事名
    [[記事名|表示文字]] -> 	表示文字
    [[記事名#節名|表示文字]] -> 表示文字
    """
    # [[記事名]] -> 記事名
    new = regex.sub(
        r"\[\["
        r"(?P<art_name>[^\|\]]+)"
        r"\]\]",
        r"\g<art_name>",
        text,
        flags=regex.MULTILINE,
    )

    new = regex.sub(
        r"\[\["
        r"(?P<art_name>[^\#\|]+)"
        r"(?:\#(?P<sec_name>[^\|]+))?"
        r"\|(?P<disp_name>.+?)"  # greedy だと　 .＋ は \]\] もマッチするのでそれを避けるために .+? にしてる!!
        r"\]\]",
        r"\g<disp_name>",
        new,
        flags=regex.MULTILINE,
    )

    return new


def remove_inner_link_27():
    """
    https://nlp100.github.io/ja/ch03.html#27-内部リンクの除去
    """
    temp_dict = remove_emp_26()
    for k, v in temp_dict.items():
        temp_dict[k] = remove_inner_link(v)

    # pprint(temp_dict)
    return temp_dict


def remove_markup_28() -> dict[str, str]:
    """
    https://nlp100.github.io/ja/ch03.html#28-mediawikiマークアップの除去
    """
    temp_dict = remove_inner_link_27()
    for k, v in temp_dict.items():
        temp_dict[k] = remove_lang_template(v)

    # pprint(temp_dict)
    return temp_dict


def extract_tmp_idx(text: str) -> list[tuple[int, int]]:
    # テンプレートは {{}} で囲まれている．
    # ただし テンプレートの内部 (content) でも {{}} が使われる可能性があるので入れ子で取得する必要がある
    double_flag_ptrn = regex.compile(
        r"(?P<template>\{\{(?P<content>(?:(?&template)|[^{}])+)\}\})",  # テンプレートを取得する regex
        flags=regex.MULTILINE | regex.DOTALL,
    )

    ret = []
    for match_ret in regex.finditer(double_flag_ptrn, text):
        ret.append((match_ret.start(), match_ret.end()))

    return ret


def remove_lang_template(text: str) -> str:
    """
    {{lang|en|United Kingdom of Great Britain and Northern Ireland}}
    -> United Kingdom of Great Britain and Northern Ireland
    """
    lang_tmp_ptrn = (
        r"\{\{lang\s*"
        r"\|(?P<lang_name>[a-z]+)"
        r"\|(?P<disp_name>.+?)"  # disp_name の部分に {{}} がこない前提
        r"\}\}"
    )

    regex.sub(lang_tmp_ptrn, r"\g<disp_name>", text)

    return regex.sub(lang_tmp_ptrn, r"\g<disp_name>", text)


def str_replace_with_ranges(text: str, start: int, end: int, new: str) -> str:
    return text[:start] + new + text[end:]


def get_country_image_29():
    """
    https://nlp100.github.io/ja/ch03.html#29-国旗画像のurlを取得する
    """
    basic_info_dict = remove_markup_28()
    count_flag_img = basic_info_dict["国旗画像"].strip()
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": "File:" + count_flag_img,
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    page = DATA["query"]["pages"]
    url: str
    for k, v in page.items():
        url = v["imageinfo"][0]["url"]
    print(url)


if __name__ == "__main__":
    get_country_image_29()
