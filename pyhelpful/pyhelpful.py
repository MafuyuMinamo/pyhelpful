import os
import re
import pathlib
import shutil
import time
from tkinter import Tk
from tkinter import filedialog
from typing import Any

from .mylogger import MyStreamLogger

log = MyStreamLogger("DEBUG")


def dialog_file_picker(init_dir: str = "", heading: str = "", types: str = "*") -> str | None:
    """ダイアログを使ったファイルパスの取得

    Args:
        init_dir (str, optional):

            ダイアログの初期フォルダのパス。

            Defaults to "".

        heading (str, optional):

            ダイアログのファイルの見出し。

            Defaults to "".

        types (str, optional):

            拡張子のフィルタ文字

            Defaults to "*".

    Returns:
        str | None: 成功したら 取得したファイルパス(str)を返す。取得できなかった場合は None
    """
    root = Tk()
    root.withdraw()
    if init_dir == "":
        initialdir = os.getcwd()
    else:
        if os.path.isdir(init_dir) is True:
            initialdir = init_dir
        else:
            initialdir = os.getcwd()
            log.warning("{} は存在しません。".format(initialdir))
    filetypes = [(heading, types)]
    path = filedialog.askopenfilename(
        filetypes=filetypes, initialdir=initialdir)
    log.debug("取得したファイルパス: {}, Type: {}".format(path, type(path)))
    root.destroy()
    if path:
        return path
    else:
        log.warning("ファイルは選択されていません。")
        return None


def dialog_folder_picker(init_dir: str = "") -> str | None:
    """ダイアログを使ったフォルダパスの取得

    Args:
        init_dir (str, optional):

            ダイアログの初期フォルダのパス。

            Defaults to "".

    Returns:
        str | None: 成功したら 取得したフォルダパス(str)を返す。取得できなかった場合は None
    """
    root = Tk()
    root.withdraw()
    if init_dir == "":
        initialdir = os.getcwd()
    else:
        if os.path.isdir(init_dir) is True:
            initialdir = init_dir
        else:
            initialdir = os.getcwd()
            log.warning("{} は存在しません。".format(initialdir))
    path = filedialog.askdirectory(initialdir=initialdir)
    log.debug("取得したフォルダパス: {}, Type: {}".format(path, type(path)))
    root.destroy()
    if path:
        return path
    else:
        log.warning("フォルダは選択されていません。")
        return None


def is_invalid_char(string: str) -> bool:
    """指定の文字列内に禁止文字が使用されているかを判定する。

    Args:
        string (str): 指定の文字列

    Returns:
        bool: 無効文字が含まれている場合は True
    """
    invalid_character = [
        "\\",
        "/",
        ":",
        "*",
        "?",
        '"',
        "<",
        ">",
        "|",
    ]

    for character in invalid_character:
        if character in string:
            return True
        else:
            pass
    return False


def replace_invalid_char(string: str, replace_char="-") -> str:
    """指定の文字列内の禁止文字を任意の文字に変換する。

    Args:
        string (str): 指定の文字列

        replace_char (str, optional):

            置き換える文字。

            Defaults to "-".

    Returns:
        str: 変換後の文字列
    """
    if is_invalid_char(replace_char) is True:
        # ? 無効文字を別の無効文字に置き換えようとした場合の処理
        log.warning('{} は無効文字です。 "-" で代用します。'.format(replace_char))
        replace_char = "-"
    else:
        pass
    return re.sub(r'[|\\|/|:|*|?|"|<|>|]', replace_char, string)


def dir_create(parent_dir_path: str, dir_name: str) -> str | None:
    """任意の場所に新規フォルダを作成する。既に存在する場合はそのまま。

    Args:
        parent_dir_path (str): 親フォルダのパス
        dir_name (str): 作成するフォルダ名

    Returns:
        str | None: 成功した場合は作成したフォルダのパス、失敗した場合は None を返す。
    """
    sub_dir = re.sub(r'[\\|/|:|*|?|"|<|>|]', "-", dir_name)
    try:
        create_dir = os.path.join(parent_dir_path, sub_dir)
        if os.path.isdir(create_dir) is True:
            log.warning("{} は既に存在します。".format(create_dir))
        else:
            pathlib.Path(create_dir).mkdir(parents=True, exist_ok=True)
            log.info("{} フォルダを新規作成しました。".format(create_dir))
        return str(create_dir)
    except:
        log.error("フォルダの新規作成に失敗しました。")
        return None


def dir_create_desktop(dir_name: str) -> str | None:
    """デスクトップに新規フォルダを作成する。

    Args:
        dir_name (str): 作成するフォルダ名

    Returns:
        str | None: 成功した場合は作成したフォルダのパス、失敗した場合は None を返す。
    """
    parent_dir_path = os.path.expanduser("~/Desktop")
    return dir_create(parent_dir_path, dir_name)


def file_create_overwrite(
    dir_path: str, file_name: str, mode: str, data: Any, eof_new_line: bool = True
) -> bool:
    """新規ファイルを作成する。既にファイルが存在する場合は上書き、または、追記をする。

    Args:
        dir_path (str): ファイルを作成するフォルダのパス
        file_name (str): 作成するファイル名
        mode (str):
            "w": 新規作成（ファイルが存在する場合は上書き）
            "a": 新規作成（ファイルの末尾から内容を追記）

        data (Any): 書き込む内容

        eof_new_line (bool, optional):
            True の場合はEOFで改行して終了する

            Defaults to True.

    Returns:
        bool: 成功したら True
    """
    if os.path.isdir(dir_path) is False:
        log.error("指定したフォルダ {} は存在しません。".format(dir_path))
        return False
    else:
        file_path = os.path.join(dir_path, file_name)

    if mode == "w" or mode == "a":
        pass
    else:
        mode = "a"
        log.warning("『mode』の指定が不正です。追記モード('a')で続行します。")

    try:
        with open(file_path, mode=mode, encoding="utf-8", newline="\n") as f:
            if eof_new_line is True:
                f.write(data + "\n")
            else:
                f.write(data)

        if mode == "w":
            log.info("ファイルの作成 / 上書きが完了しました。")
        elif mode == "a":
            log.info("ファイルへの追記が完了しました。")
        return True
    except:
        log.error("処理に失敗しました。")
        return False


def file_copy(ref_file_path: str, target_dir_path: str, copy_as: bool = False) -> bool:
    """ファイルのコピー。コピー先のフォルダは先に作っておくこと。

    Args:
        ref_file_path (str): コピー元のファイルパス
        target_dir_path (str): コピー先のフォルダパス
        copy_as (bool): 指定のコピー先に既に同名のファイルがあった場合の処理分岐
            True: ファイル名の末尾に "_unixtime"をつけてコピーを作成する
            False: コピーしない

            Defaults to False.

    Returns:
        bool: 成功したら True
    """
    if os.path.isfile(ref_file_path) is False:
        log.error("指定のファイルは存在しません。")
        log.error("コピー元: {}".format(ref_file_path))
        return False
    else:
        pass

    if os.path.isdir(target_dir_path) is False:
        log.error("指定のコピー先フォルダは存在しません。")
        log.error("コピー先: {}".format(target_dir_path))
        return False
    else:
        pass

    ref_file_name = os.path.basename(ref_file_path)
    ext_name_tuple = os.path.splitext(ref_file_path)
    if os.path.isfile(os.path.join(target_dir_path, ref_file_name)) is True:

        if copy_as is False:
            log.error("指定のコピー先フォルダには、既に同名のファイルが存在します。")
            return False

        elif copy_as is True:
            target_dir_path = os.path.join(
                target_dir_path,
                ref_file_name[:-4] + "_" +
                str(int(time.time())) + ext_name_tuple[-1],
            )
            log.warning("指定のコピー先フォルダには、既に同名のファイルが存在します。")
            log.warning(
                "引数: copy_as = True のため、ファイル末尾にUNIX時間を追加してコピーします。"
            )
            log.warning(target_dir_path)
    else:
        pass

    try:
        shutil.copy(ref_file_path, target_dir_path)
        log.info("ファイルのコピーが完了しました。")
        return True
    except:
        log.error("処理に失敗しました。")
        return False


def dir_copy(ref_dir_path: str, target_dir_path: str) -> bool:
    """
    フォルダのコピー。

    コピー先に既に同名のフォルダがある場合は処理しない。（上書き保存はしない）

    Args:
        ref_dir_path (str): コピー元のフォルダパス
        target_dir_path (str): コピー先のフォルダパス

    Returns:
        bool: 成功したら True
    """
    if os.path.isdir(ref_dir_path) is False:
        log.error("指定のコピー元フォルダは存在しません。")
        log.error("コピー元: {}".format(ref_dir_path))
        return False
    else:
        pass
    if os.path.isdir(target_dir_path) is True:
        log.error("指定のコピー先には、既に同じ名前のフォルダが存在します。")
        log.error("コピー先: {}".format(target_dir_path))
        return False
    else:
        pass

    try:
        shutil.copytree(ref_dir_path, target_dir_path)
        log.info("フォルダのコピーが完了しました。")
        return True
    except:
        log.error("処理に失敗しました。")
        return False


def file_delete(file_path: str) -> bool:
    """ファイルの削除

    Args:
        file_path (str): 削除するファイルのパス

    Returns:
        bool: 成功したら True
    """
    if os.path.isfile(file_path) is False:
        log.error("指定のファイルは存在しません。")
        return False
    else:
        try:
            os.remove(file_path)
            log.info("ファイルの削除が完了しました。")
            return True
        except:
            log.error("処理に失敗しました。")
            return False


def dir_delete(dir_path: str) -> bool:
    """フォルダの削除

    Args:
        dir_path (str): 削除するフォルダのパス

    Returns:
        bool: 成功したら True
    """
    if os.path.isdir(dir_path) is False:
        log.error("指定のフォルダは存在しません。")
        return False
    else:
        try:
            shutil.rmtree(dir_path)
            log.info("フォルダ {} の削除が完了しました。".format(dir_path))
            return True
        except:
            log.error("処理に失敗しました。")
            return False


def get_info_dir_file_ext(file_path: str, info: str) -> str | bool:
    """パス文字列から、フォルダ名、ファイル名、拡張子を取得する

    Args:
        file_path (str): 任意のファイルパス

        info (str): 取得する情報
            "dir_name": フォルダ名
            "file_name": ファイル名
            "ext_name": 拡張子名
            "file_name_non_ext": 拡張子なしのファイル名

    Returns:
        str | bool: 成功したら 指定の情報の文字列を返す。失敗した場合は False
    """
    if os.path.isfile(file_path) is False:
        log.error("指定のファイルは存在しません。")
        return False
    else:
        try:
            dir_name = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            ext_name_tuple = os.path.splitext(file_path)
            ext_name = ext_name_tuple[-1]
            file_name_non_ext = file_name[: (-1 * len(ext_name))]
            if info == "dir_name":
                log.info("dir name: {}".format(dir_name))
                return dir_name
            elif info == "file_name":
                log.info("file name: {}".format(file_name))
                return file_name
            elif info == "ext_name":
                log.info("ext name: {}".format(ext_name))
                return ext_name
            elif info == "file_name_non_ext":
                log.info("file name non ext: {}".format(file_name_non_ext))
                return file_name_non_ext
            else:
                log.error("info の引数が不正です。")
                return False
        except:
            log.error("処理に失敗しました。")
            return False


def get_file_list(dir_path: str) -> tuple | bool:
    """任意のフォルダにあるファイルの一覧を取得

    Args:
        dir_path (str): 任意のフォルダパス

    Returns:
        tuple | bool: 成功したら ファイル一覧のタプルを返す。失敗した場合は False
    """
    file_list_all = []
    if os.path.isdir(dir_path) is False:
        log.error("指定のフォルダは存在しません。")
        return False
    else:
        try:
            for current_dir, sub_dirs, files_list in os.walk(dir_path):
                for file_name in files_list:
                    file_list_all.append(os.path.join(current_dir, file_name))
            log.info("ファイル数: {}".format(len(file_list_all)))
            return tuple(file_list_all)
        except:
            log.error("処理に失敗しました。")
            return False
