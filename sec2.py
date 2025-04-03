import os
import sys
from pprint import pprint


def get_file() -> int:
    return os.system(
        "curl https://nlp100.github.io/data/popular-names.txt -o src/popular-names.txt"
    )


def get_lines() -> list[str]:
    """
    `src/popular-names.txt`
    の中身を 行のリストとして返す
    """
    path = "src/popular-names.txt"
    f = open(path, "r")
    lines = f.readlines()
    f.close()

    return lines


def get_data() -> str:
    """
    `src/popular-names.txt`
    の中身を返す
    """
    path = "src/popular-names.txt"
    f = open(path, "r")
    data = f.read()
    f.close()

    return data


def line_count_10():
    """
    https://nlp100.github.io/ja/ch02.html#10-行数のカウント

    確認には

    ```
    wc -l src/popular-names.txt
    ```

    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()
    print(len(lines))


def tab_to_space_11() -> str:
    """
    https://nlp100.github.io/ja/ch02.html#11-タブをスペースに置換

    確認には

    ```
    sed -e 's/\t/ /g' src/popular-names.txt
    ```

    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    data = get_data()

    replaced = data.replace("\t", " ")
    print(replaced)
    return replaced


def col_files_12():
    """
    https://nlp100.github.io/ja/ch02.html#12-1列目をcol1txtに2列目をcol2txtに保存


    確認には
    ```
    diff src/col1.txt <(cut -f 1 src/popular-names.txt)
    diff src/col2.txt <(cut -f 2 src/popular-names.txt)
    ```
    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()

    mat = [list(map(lambda col: col.strip("\n"), line.split("\t"))) for line in lines]
    col1 = [r[0] for r in mat]
    col2 = [r[1] for r in mat]

    col1_s = "\n".join(col1) + "\n"  # 行末の改行
    print(col1_s)
    col1f = open("src/col1.txt", "w")
    col1f.write(col1_s)
    col1f.close()

    col2_s = "\n".join(col2) + "\n"  # 行末の改行
    print(col2_s)
    col2f = open("src/col2.txt", "w")
    col2f.write(col2_s)
    col2f.close()


def get_col1_col2_lines() -> tuple[list[str], list[str]]:
    col1f = open("src/col1.txt", "r")
    col2f = open("src/col2.txt", "r")
    ret = (col1f.readlines(), col2f.readlines())
    col1f.close()
    col2f.close()

    return ret


def col_merge_13():
    """
    https://nlp100.github.io/ja/ch02.html#13-col1txtとcol2txtをマージ

    確認には
    ```
    diff src/col1_col2_concat.txt <(paste src/col1.txt src/col2.txt)
    ```
    を使うこと
    """
    # col_files_12()
    (col1_lines, col2_lines) = get_col1_col2_lines()
    col1_lines_stripped = [line.strip() for line in col1_lines]
    col2_lines_stripped = [line.strip() for line in col2_lines]

    rows = []
    for c1, c2 in zip(col1_lines_stripped, col2_lines_stripped):
        rows.append("\t".join([c1, c2]))

    ret = "\n".join(rows) + "\n"  # 行末の改行

    col1_col2_concatf = open("src/col1_col2_concat.txt", "w")
    col1_col2_concatf.write(ret)
    col1_col2_concatf.close()


def head_lines_14():
    """
    https://nlp100.github.io/ja/ch02.html#14-先頭からn行を出力

    確認には
    ```
    head -n src/popular-names.txt
    ```
    を使うこと
    """
    if len(sys.argv) < 2:
        return
    n = int(sys.argv[1])
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()
    ret = "".join(lines[0:n])
    print(ret)


def tail_lines_15():
    """
    https://nlp100.github.io/ja/ch02.html#15-末尾のn行を出力

    確認には
    ```
    tail -n src/popular-names.txt
    ```
    を使うこと
    """
    if len(sys.argv) < 2:
        return
    n = int(sys.argv[1])
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()

    ret = "".join(lines[len(lines) - n :])
    print(ret)


def file_split_16():
    """
    https://nlp100.github.io/ja/ch02.html#16-ファイルをn分割する

    確認には
    ```
    split -l $(($(cat src/popular-names.txt | wc -l) / n)) src/popular-names.txt
    ```
    を使うこと
    """
    if len(sys.argv) < 2:
        return
    n = int(sys.argv[1])
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()
    line_num = len(lines)
    chunk_size = (line_num + 1) // n

    rets = []
    for i in range(n):
        rets.append(
            "".join(lines[i * chunk_size : min((i + 1) * chunk_size, line_num)])
        )

    for i, ret in enumerate(rets):
        print(f"file {i}")
        print(ret)


def name_set_17():
    """
    https://nlp100.github.io/ja/ch02.html#17-１列目の文字列の異なり

    確認には
    ```
    cut -f 1 src/popular-names.txt | sort | uniq
    ```
    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()

    mat = [list(map(lambda col: col.strip("\n"), line.split("\t"))) for line in lines]
    col1 = [r[0] for r in mat]
    name_set = set(col1)
    pprint(name_set)


def col_sort_18():
    """
    https://nlp100.github.io/ja/ch02.html#18-各行を3コラム目の数値の降順にソート
    確認には
    ```
    sort -k 3,3nr src/popular-names.txt
    ```
    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()

    mat = [list(map(lambda col: col.strip("\n"), line.split("\t"))) for line in lines]
    pprint(sorted(mat, reverse=True, key=lambda row: int(row[2])))


def freq_19():
    """
    https://nlp100.github.io/ja/ch02.html#19-各行の1コラム目の文字列の出現頻度を求め出現頻度の高い順に並べる

    確認には
    ```
    cut -f 1 src/popular-names.txt | sort | uniq -c | sort -r
    ```
    を使うこと
    """
    if get_file() != 0:
        print("failed to get file")
        return
    lines = get_lines()
    mat = [list(map(lambda col: col.strip("\n"), line.split("\t"))) for line in lines]
    col1 = [r[0] for r in mat]
    name_set = set(col1)
    name_histgram: list[tuple[str, int]] = []

    for name in name_set:
        name_histgram.append((name, col1.count(name)))

    sorted_histgram = sorted(name_histgram, key=lambda data: data[1], reverse=True)
    for name, num in sorted_histgram:
        print("{:>4} {}".format(num, name))


if __name__ == "__main__":
    freq_19()
