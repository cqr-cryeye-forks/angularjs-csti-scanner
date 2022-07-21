import os
import sys

import colorlog


class FileLoggingHelper:
    """The FileLoggingHelper enables logging messages to a file.

    _phantomjs_driver (str): The cached path to the executable PhantomJS driver.

    """

    __filename = None

    @staticmethod
    def set_file(filename=None):
        """Set the filename to log messages to.

        Args:
            filename (str): The filename (including absolute or relative path) to log to.

        Note:
            If the log filename already exists it will be appended with a number. So output.log
            could become `output.log.1` or `output.log.2`.

        """

        if not filename:
            return

        filename_backup = filename
        filename_append = 0
        filename_changed = False
        filename_error = False

        while os.path.isfile(filename) and not filename_error:
            filename_changed = True
            filename_append += 1
            filename = f"{filename_backup}.{filename_append}"

            if filename_append == sys.maxsize:
                filename_error = True

        if filename_error:
            colorlog.getLogger().error("The output log file already exists and therefore no logs will be written.")
            return

        if filename_changed:
            colorlog.getLogger().warning(
                f"The output log filename was changed to `{filename}` since `{filename_backup}` already exists.")

        FileLoggingHelper.__filename = filename

    @staticmethod
    def log(message):
        """Write the given message to the initialized log file.

        Args:
            message (str): The message to write to the log file.

        """

        if not FileLoggingHelper.__filename:
            return

        with open(FileLoggingHelper.__filename, "a") as log:
            log.write(message + "\n")
