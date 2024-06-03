# Python helpful functions

## Overview

概要

- このモジュールは、『ルーチンワーク的なパソコンの事務作業を半自動化する時によく使う機能』をまとめたものです。

  - ダイアログを使ったファイル・フォルダのパスの取得する
  - 任意の文字列に対して、使用禁止文字の有無を判定する
  - 使用禁止文字を任意の文字列へ置き換える
  - 任意の場所に新規フォルダを作成する
  - 新規ファイルの作成・上書き・追記
  - ファイル・フォルダのコピーと削除
  - パス文字列から、フォルダ名、ファイル名、拡張子を取得する
  - 任意のフォルダにあるファイルの一覧を取得する

- こういった機能は標準ライブラリを使って実現するわけですが、案件の度にコードを探してきてコピペするのも手間ですよね。なので、まとめておきました！

## Usage

使い方

### Installation

インストール方法

`pip install git+https://github.com/MafuyuMinamo/pyhelpful.git`

### functions

各関数の解説

#### `dialog_file_picker`

- summary
  - ダイアログを使ってファイルパスを取得する。

- args
  - `init_dir` (str, optional): ダイアログの初期フォルダのパス（デフォルトは `""`）
  - `heading` (str, optional): ダイアログのファイルの見出し（デフォルトは `""`）
  - `types` (str, optional): 拡張子のフィルタ文字（デフォルトは `"*"`）

- return
  - `str | None`: 取得したファイルパス(str)を返す。取得できなかった場合は `None`

#### `dialog_folder_picker`

- summary
  - ダイアログを使ってフォルダパスを取得する。

- args
  - `init_dir` (str, optional): ダイアログの初期フォルダのパス（デフォルトは `""`）

- return
  - `str | None`: 取得したファイルパス(str)を返す。取得できなかった場合は `None`

#### `is_invalid_char`

- summary
  - 指定の文字列内に禁止文字が使用されているかを判定する。

- args
  - `string` (str): 指定の文字列

- return
  - `bool`: 無効文字が含まれている場合は `True`

#### `replace_invalid_char`

- summary
  - 指定の文字列内の禁止文字を任意の文字に変換する。

- args
  - `string` (str): 指定の文字列
  - `replace_char` (str, optional): 置き換える文字（デフォルトは `"-"`）

- return
  - `bool`: 無効文字が含まれている場合は `True`

#### `dir_create`

- summary
  - 任意の場所に新規フォルダを作成する。既に存在する場合はそのまま。

- args
  - `parent_dir_path` (str): 親フォルダのパス
  - `dir_name` (str): 作成するフォルダ名

- return
  - `str | None`: 成功した場合は作成したフォルダのパス、失敗した場合は `None`

#### `dir_create_desktop`

- summary
  - デスクトップに新規フォルダを作成する。既に存在する場合はそのまま。

- args
  - `dir_name` (str): 作成するフォルダ名

- return
  - `str | None`: 成功した場合は作成したフォルダのパス、失敗した場合は `None`

#### `file_create_overwrite`

- summary
  - 新規ファイルを作成する。既にファイルが存在する場合は上書き、または、追記をする。

- args
  - `dir_path` (str): ファイルを作成するフォルダのパス
  - `file_name` (str): 作成するファイル名
  - `mode` (str):
    - `"w"`: 新規作成（ファイルが存在する場合は上書き）
    - `"a"`: 新規作成（ファイルの末尾から内容を追記）
  - `data` (Any): 書き込む内容
  - `eof_new_line` (bool, optional): `True` の場合はEOFで改行して終了する（デフォルトは `True`）

- return
  - `bool`: 成功したら `True`

#### `file_copy`

- summary
  - ファイルのコピー。コピー先のフォルダは先に作っておくこと。

- args
  - `ref_file_path` (str): コピー元のファイルパス
  - `target_dir_path` (str): コピー先のフォルダパス
  - `copy_as` (bool): 指定のコピー先に既に同名のファイルがあった場合の処理分岐
    - `True`: ファイル名の末尾に "_unixtime"をつけてコピーを作成する
    - `False`: コピーしない（デフォルト）

- return
  - `bool`: 成功したら `True`

#### `dir_copy`

- summary
  - フォルダのコピー。上書き保存はしない。
  - （コピー先に既に同名のフォルダがある場合は処理しない）

- args
  - `ref_dir_path` (str): コピー元のフォルダパス
  - `target_dir_path` (str): コピー先のフォルダパス

- return
  - `bool`: 成功したら `True`

#### `file_delete`

- summary
  - ファイルの削除。

- args
  - `file_path` (str): 削除するファイルのパス

- return
  - `bool`: 成功したら `True`

#### `dir_delete`

- summary
  - フォルダの削除。

- args
  - `file_path` (str): 削除するファイルのパス

- return
  - `bool`: 成功したら `True`

#### `get_info_dir_file_ext`

- summary
  - パス文字列から、フォルダ名、ファイル名、拡張子を取得する。

- args
  - `file_path` (str): 任意のファイルパス
  - `info` (str): 取得する情報
    - `"dir_name"`: フォルダ名
    - `"file_name"`: ファイル名
    - `"ext_name"`: 拡張子名
    - `"file_name_non_ext"`: 拡張子なしのファイル名

- return
  - `str | bool`: 成功したら 指定の情報の文字列を返す。失敗した場合は `False`

#### `get_file_list`

- summary
  - 任意のフォルダにあるファイルの一覧を取得する。

- args
  - `dir_path` (str): 任意のフォルダパス

- return
  - `tuple | bool`: 成功したら ファイル一覧のタプルを返す。失敗した場合は `False`

### Examples of use

コーディング例

```text
Work in progress.
```

### Uninstallation

アンイストール方法

`pip uninstall pyhelpful`

## Dependencies

依存関係の表記

- None
