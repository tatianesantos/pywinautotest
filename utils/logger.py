"""Logging functionalities."""
import logging


class Logger(object):
    """Class encapsulating logging functionalities."""

    def __init__(self, path="root.log", name="root", level="info"):
        self.logger = logging.getLogger(name)
        self._configure_logging(path, level)

    def _configure_logging(self, path, level):
        """Configure the file logger."""
        logging_format = (
            "%(asctime)s : %(levelname)s : %(module)s.%(lineno)s : %(message)s"
        )
        date_format = "%Y/%m/%d %I:%M:%S %p"

        log_formatter = logging.Formatter(logging_format, date_format)
        file_handler = logging.FileHandler(path, mode="w", encoding="UTF-8")
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(self._logging_levels(level))

    def _logging_levels(self, level):
        """Return logging level by given parameter.

        Parameters
        ----------
        level: str
            Threshold for the logger. Logging messages which are less severe
            than level will be ignored (debug, info, warning, error and
            critical).
        """
        levels = {
            "info": logging.INFO,
            "error": logging.ERROR,
            "debug": logging.DEBUG,
            "warning": logging.WARNING,
            "critical": logging.CRITICAL,
        }
        return levels[level]
