import logging
import inspect
import os


class MyStreamLogger:

    LOGGER_FOMAT: str = "[%(asctime)s] [%(name)s] [%(levelname)s: %(message)s]"

    def __init__(self, set_level: str = "DEBUG"):
        """ターミナルにログメッセージを出力する。

        Args:
            set_level (str, optional):

            "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" から選択。

            Defaults to "DEBUG".
        """
        self._level_format_setting(set_level)

    def _level_format_setting(self, set_level: str):
        """ロガーの出力レベルとフォーマットの設定"""

        if set_level == "CRITICAL":
            level = logging.CRITICAL
        elif set_level == "ERROR":
            level = logging.ERROR
        elif set_level == "WARNING":
            level = logging.WARNING
        elif set_level == "INFO":
            level = logging.INFO
        else:
            level = logging.DEBUG

        self.logger = logging.basicConfig(
            level=level,
            format=self.LOGGER_FOMAT,
        )

    def trace(log_func):
        """ログ出力指示の記載場所（コードのファイル名と行番号、その関数・メソッド名）を取得するデコレータ

        Args:
            log_func (function): 各レベルのログを出力するメソッド
        """

        def get_location(self, msg: str):
            frame = inspect.currentframe().f_back
            self.location = 'Location >> {}:{}, function/method name: "{}"'.format(
                os.path.basename(frame.f_code.co_filename),
                frame.f_lineno,
                frame.f_code.co_name,
            )
            self.logger = logging.getLogger(self.location)
            log_func(self, msg)

        return get_location

    @trace
    def debug(self, msg: str):
        self.logger.debug("Message >> " + str(msg))

    @trace
    def info(self, msg: str):
        self.logger.info("Message >> " + str(msg))

    @trace
    def warning(self, msg: str):
        self.logger.warning("Message >> " + str(msg))

    @trace
    def error(self, msg: str):
        self.logger.error("Message >> " + str(msg))

    @trace
    def critical(self, msg: str):
        self.logger.critical("Message >> " + str(msg))


class MyFileLogger(MyStreamLogger):

    LOGGER_FOMAT: str = "[%(asctime)s] [%(name)s] [%(levelname)s: %(message)s]"

    def __init__(self, log_file_path: str, set_level: str = "DEBUG"):
        """ターミナルにログメッセージを出力する。さらに、指定のログファイルにも出力する。

        Args:
            log_file_path (str): ログファイルのフルパス

            set_level (str, optional):

                "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" から選択。

                Defaults to "DEBUG".
        """
        self._level_format_setting(set_level)
        self.log_file_path = log_file_path

    def trace(log_func):
        """ログ出力指示の記載場所（コードのファイル名と行番号、その関数・メソッド名）を取得するデコレータ

        Args:
            log_func (function): 各レベルのログを出力するメソッド
        """

        def get_location(self, msg: str):
            frame = inspect.currentframe().f_back
            _dir = os.path.dirname(frame.f_code.co_filename)
            _file = os.path.basename(frame.f_code.co_filename)
            _file_path = os.path.join(_dir, _file)
            self.location = 'Location >> {}:{}, function/method name: "{}"'.format(
                _file_path,
                frame.f_lineno,
                frame.f_code.co_name,
            )
            self.logger = logging.getLogger(self.location)
            file_handler = logging.FileHandler(
                filename=self.log_file_path,
                encoding="utf-8",
            )
            file_handler.setFormatter(logging.Formatter(self.LOGGER_FOMAT))
            self.logger.addHandler(file_handler)
            log_func(self, msg)

        return get_location

    @trace
    def debug(self, msg: str):
        self.logger.debug("Message >> " + msg)

    @trace
    def info(self, msg: str):
        self.logger.info("Message >> " + msg)

    @trace
    def warning(self, msg: str):
        self.logger.warning("Message >> " + msg)

    @trace
    def error(self, msg: str):
        self.logger.error("Message >> " + msg)

    @trace
    def critical(self, msg: str):
        self.logger.critical("Message >> " + msg)
