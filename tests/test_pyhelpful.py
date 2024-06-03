import os
import pathlib
import glob
import tempfile

from pyhelpful.pyhelpful import dialog_file_picker
from pyhelpful.pyhelpful import dialog_folder_picker
from pyhelpful.pyhelpful import is_invalid_char
from pyhelpful.pyhelpful import replace_invalid_char
from pyhelpful.pyhelpful import dir_create
from pyhelpful.pyhelpful import dir_delete
from pyhelpful.pyhelpful import file_create_overwrite
from pyhelpful.pyhelpful import file_delete
from pyhelpful.pyhelpful import file_copy
from pyhelpful.pyhelpful import dir_copy
from pyhelpful.pyhelpful import get_info_dir_file_ext
from pyhelpful.pyhelpful import get_file_list

from pyhelpful.mylogger import MyStreamLogger

test_log = MyStreamLogger("DEBUG")


def test_dialog_file_picker_file_select():
    """ファイルを選択すると、そのファイルのパス(str)が返ってくる。"""
    expected = type("file path strings")
    test_log.debug("適当なファイルを選択してください。")
    assert type(dialog_file_picker()) == expected


def test_dialog_file_picker_file_not_select():
    """ファイルを選択せずにダイアログを閉じたりキャンセルした場合は None が返ってくる。"""
    expected = type(None)
    test_log.debug("『閉じる』または『キャンセル』を押してください。")
    assert type(dialog_file_picker()) == expected


def test_dialog_folder_picker_folder_select():
    """フォルダを選択すると、そのファイルのパス(str)が返ってくる。"""
    expected = type("folder path strings")
    test_log.debug("適当なフォルダを選択してください。")
    assert type(dialog_folder_picker()) == expected


def test_dialog_folder_picker_folder_not_select():
    """フォルダを選択せずにダイアログを閉じたりキャンセルした場合は None が返ってくる。"""
    expected = type(None)
    test_log.debug("『閉じる』または『キャンセル』を押してください。")
    assert type(dialog_folder_picker()) == expected


def test_is_invalid_char():
    """無効文字が含まれている場合は True, 含まれていない場合は False を返す。"""

    # * 想定される禁止文字の一覧
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

    strings = "abc"
    assert is_invalid_char(strings) is False

    ex_strings = "C:\Apps"
    assert is_invalid_char(ex_strings) is True

    for i_char in invalid_character:
        assert is_invalid_char(strings + i_char) is True


def test_replace_invalid_char():
    """指定の文字列内の禁止文字を任意の文字に変換。"""

    # * 想定される禁止文字の一覧
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

    # * 禁止文字が含まれていない場合は、文字列はそのまま維持される
    strings = "abc"
    assert replace_invalid_char(strings) == strings

    # * 引数で特に指定しない場合は、禁止文字は "-" に置き換えられる
    ex_strings = "abcd:efgh"
    assert replace_invalid_char(ex_strings) == "abcd-efgh"

    # * 禁止文字を別の禁止文字に置き換えようとした場合は、"-" で代用される
    assert replace_invalid_char(ex_strings, "?") == "abcd-efgh"
    assert replace_invalid_char(ex_strings, "?[") == "abcd-efgh"

    for i_char in invalid_character:
        assert replace_invalid_char(
            "abcd" + i_char + "efgh", "_re_") == "abcd_re_efgh"


def test_dir_create_delete():
    """フォルダの作成と削除。"""

    with tempfile.TemporaryDirectory() as td:

        test_main_dir_path = td
        test_dir_name = "temp_for_test_abc"
        test_create_dir = os.path.join(test_main_dir_path, test_dir_name)

        # * ファルダの新規作成が成功したら、そのパスが返ってくる
        assert dir_create(test_main_dir_path, test_dir_name) == test_create_dir

        # * 作成されたことを確認
        assert os.path.isdir(test_create_dir) is True

        # * 既にフォルダが存在する場合はそのまま
        assert dir_create(test_main_dir_path, test_dir_name) == test_create_dir

        # * 存在していることを確認
        assert os.path.isdir(test_create_dir) is True

        # * 親フォルダが存在しない場合は、まずは親フォルダを準備して、そこに新規フォルダが作成される
        non_existent_dir = os.path.join(test_main_dir_path, "non_for_test_abc")
        expected = os.path.join(non_existent_dir, test_dir_name)

        # * ファルダの新規作成が成功したら、そのパスが返ってくる
        assert dir_create(non_existent_dir, test_dir_name) == expected

        # * 作成されたことを確認
        assert os.path.isdir(expected) is True

        # * フォルダの削除が成功したら True
        assert dir_delete(test_create_dir) is True

        # * 削除されたかを確認
        assert os.path.isdir(test_create_dir) is False

        # * 存在しないフォルダを削除しようとした場合は False
        assert dir_delete(test_create_dir) is False


def test_file_create_overwrite_delete():
    """ファイルの作成（上書き、追記）と削除。"""

    with tempfile.TemporaryDirectory() as td:
        dir_path = td
        file_name = "temp_for_test_abc.txt"
        data_0 = "test_strings_0"
        data_1 = "test_strings_1"
        data_2 = "test_strings_2"
        dummy_dir = os.path.join(dir_path, "abc")

        # * ファイルの新規作成が成功したら True が返ってくる
        # * 1行目
        assert file_create_overwrite(dir_path, file_name, "w", data_0) is True

        # * 追記モード
        # * 2行目
        assert file_create_overwrite(dir_path, file_name, "a", data_1) is True

        # * 追記モードで、EOFで改行しない
        # * 3行目（EOFで改行しないので、4行目は存在しない）
        assert (
            file_create_overwrite(
                dir_path,
                file_name,
                "a",
                data_2,
                eof_new_line=False,
            )
            is True
        )

        # * 作成したファイルの存在確認
        assert os.path.isfile(os.path.join(dir_path, file_name)) is True

        # * ファイルの中身を確認
        if os.path.isfile(os.path.join(dir_path, file_name)) is True:
            with open(os.path.join(dir_path, file_name)) as f:
                lines = f.read().splitlines()
            assert lines[0] == data_0
            assert lines[1] == data_1
            assert lines[2] == data_2
            assert len(lines) == 3

        # * 存在しないフォルダにファイルを新規作成しようとしたら False が返ってくる
        assert file_create_overwrite(
            dummy_dir, file_name, "w", data_0) is False

        # * ファイルが作成できなかったことを確認
        assert os.path.isfile(os.path.join(dummy_dir, file_name)) is False

        # * ファイルの削除
        assert file_delete(os.path.join(dir_path, file_name)) is True

        # * ファイルが削除できたことを確認
        assert os.path.isfile(os.path.join(dir_path, file_name)) is False


def test_file_dir_copy():
    """ファイル、フォルダのコピー"""

    with tempfile.TemporaryDirectory() as td:
        temp_dir_path = os.path.join(td, "temp_for_test_abc")
        ref_dir_path = os.path.join(temp_dir_path, "ref")
        target_dir_path = os.path.join(temp_dir_path, "target")
        file_name = "ref_file_for_test_abc.txt"
        ref_file_path = os.path.join(ref_dir_path, file_name)

        # * テストで使用するフォルダを作成
        pathlib.Path(ref_dir_path).mkdir(parents=True, exist_ok=True)

        # * テストで使用するファイルを作成
        with open(ref_file_path, mode="w") as f:
            f.write("")

        assert os.path.isdir(ref_dir_path) is True

        # * 『ref』フォルダを『target』フォルダとして中身をコピーする
        assert dir_copy(ref_dir_path, target_dir_path) is True

        # * コピーしたフォルダの存在確認
        assert os.path.isdir(target_dir_path) is True

        # * 『ref_file_for_test_abc.txt』を親フォルダにコピーする
        assert file_copy(ref_file_path, temp_dir_path) is True

        # * コピーしたファイルの存在確認
        assert os.path.isfile(os.path.join(temp_dir_path, file_name)) is True

        # * copy_as = False であれば、コピー先に同名のファイルがあった場合はコピーしない（上書きしない）
        assert file_copy(ref_file_path, temp_dir_path) is False

        # * copy_as = True であれば、ファイル末尾にUNIX時間を追加してコピーする
        assert file_copy(ref_file_path, temp_dir_path, copy_as=True) is True

        # * 別名コピーしたファイルの存在確認（ここまで上手くいっていれば、テキストファイルは2個ある）
        assert len(glob.glob(temp_dir_path + "/*.txt")) == 2


def test_get_info_dir_file_ext():
    """パス文字列から、フォルダ名、ファイル名、拡張子を取得"""

    file_path = os.path.abspath(__file__)
    test_log.debug(file_path)

    # * 指定したファイルが存在しない場合は False
    assert get_info_dir_file_ext("dummy_dir_path", info="file_name") is False

    # * 指定したファイルの名前
    assert get_info_dir_file_ext(
        file_path, info="file_name") == "test_pyhelpful.py"

    # * 指定したファイルの拡張子
    assert get_info_dir_file_ext(file_path, info="ext_name") == ".py"

    # * 指定したファイルの名前（拡張子なし）
    assert (
        get_info_dir_file_ext(
            file_path, info="file_name_non_ext") == "test_pyhelpful"
    )

    # * 引数 info が不正な場合は False
    assert get_info_dir_file_ext(file_path, info="dummy") is False


def test_get_file_list():
    """任意のフォルダにあるファイルの一覧を取得"""

    file_path = os.getcwd()

    # * 成功の場合はファイル一覧のタプルが帰ってくる
    assert type(get_file_list(file_path)) == tuple
