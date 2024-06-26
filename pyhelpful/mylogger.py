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

        self.set_level = set_level

    def trace(log_func):
        """ログ出力指示の記載場所（コードのファイル名と行番号、その関数・メソッド名）を取得するデコレータ

        Args:
            log_func (function): 各レベルのログを出力するメソッド
        """

        def get_location(self, msg: str | tuple | list):
            frame = inspect.currentframe().f_back
            self.location = 'Location >> {}:{}, function/method name: "{}"'.format(
                os.path.basename(frame.f_code.co_filename),
                frame.f_lineno,
                frame.f_code.co_name,
            )
            self.logger = logging.getLogger(self.location)

            if self.set_level == "CRITICAL":
                self.logger.setLevel(logging.CRITICAL)
            elif self.set_level == "ERROR":
                self.logger.setLevel(logging.ERROR)
            elif self.set_level == "WARNING":
                self.logger.setLevel(logging.WARNING)
            elif self.set_level == "INFO":
                self.logger.setLevel(logging.INFO)
            else:
                self.logger.setLevel(logging.DEBUG)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(self.LOGGER_FOMAT))
            self.logger.addHandler(stream_handler)

            log_func(self, msg)

        return get_location

    @staticmethod
    def _msg_options(msg: str | tuple | list):
        if type(msg) == tuple or type(msg) == list:
            return "Iterator >> {}".format(msg)
        else:
            return "Message >> {}".format(msg)

    @trace
    def debug(self, msg: str | tuple | list):
        self.logger.debug(self._msg_options(msg))

    @trace
    def info(self, msg: str | tuple | list):
        self.logger.info(self._msg_options(msg))

    @trace
    def warning(self, msg: str | tuple | list):
        self.logger.warning(self._msg_options(msg))

    @trace
    def error(self, msg: str | tuple | list):
        self.logger.error(self._msg_options(msg))

    @trace
    def critical(self, msg: str | tuple | list):
        self.logger.critical(self._msg_options(msg))


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

        self.set_level = set_level
        self.log_file_path = log_file_path

    def trace(log_func):
        """ログ出力指示の記載場所（コードのファイル名と行番号、その関数・メソッド名）を取得するデコレータ

        Args:
            log_func (function): 各レベルのログを出力するメソッド
        """

        def get_location(self, msg: str | tuple | list):
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

            if self.set_level == "CRITICAL":
                self.logger.setLevel(logging.CRITICAL)
            elif self.set_level == "ERROR":
                self.logger.setLevel(logging.ERROR)
            elif self.set_level == "WARNING":
                self.logger.setLevel(logging.WARNING)
            elif self.set_level == "INFO":
                self.logger.setLevel(logging.INFO)
            else:
                self.logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(
                filename=self.log_file_path,
                encoding="utf-8",
            )
            file_handler.setFormatter(logging.Formatter(self.LOGGER_FOMAT))
            self.logger.addHandler(file_handler)

            log_func(self, msg)
            file_handler.close()

        return get_location

    @trace
    def debug(self, msg: str | tuple | list):
        self.logger.debug(self._msg_options(msg))

    @trace
    def info(self, msg: str | tuple | list):
        self.logger.info(self._msg_options(msg))

    @trace
    def warning(self, msg: str | tuple | list):
        self.logger.warning(self._msg_options(msg))

    @trace
    def error(self, msg: str | tuple | list):
        self.logger.error(self._msg_options(msg))

    @trace
    def critical(self, msg: str | tuple | list):
        self.logger.critical(self._msg_options(msg))
