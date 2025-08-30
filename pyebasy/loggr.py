
import logging
from typing import Literal, Tuple

########################################################################################################################
# verbocities (abstract concept over the logging levels)
# quiet (no infos, only errors)
QUIET_VERBOCITY = 'quiet'
# normal (only overal messages are printed, logs also detailed)
NORMAL_VERBOCITY = 'normal'
# verbose (informative messages are printed, technical logged)
VERBOSE_VERBOCITY = 'verbose'
# tracing (detailed messages are printed, technical logged)
TRACING_VERBOCITY = 'tracing'

# the list of all the verbocities
VERBOCITIES = [TRACING_VERBOCITY, VERBOSE_VERBOCITY, NORMAL_VERBOCITY, QUIET_VERBOCITY]

# technical log level: the uneccesairly detailed informations (low-level details, possibly raw data from the external sources)
LVL_NAME_TECHINICAL = 'TECHNICAL'
# detailed log level: detailed information of some particular task ("processing thing X", "X got processed into Y")
LVL_NAME_DETAILED = 'DETAILED'
# informative log level: deeper into the informative ("starting to do X because Y is Z", "skpiing X because")
LVL_NAME_INFORMATIVE = 'INFORMATIVE'
# overall log level: only a brief overall progress information ("starting to do X", "X completed", ...)
LVL_NAME_OVERALL = 'OVERALL'
# warnings log level: a possible or not serious issue
LVL_NAME_WARNING = 'WARNING'
# errors log level: do I really need to explain that?
LVL_NAME_ERROR = 'ERROR'

# the custom logging levels mapping
LEVELS = {
    LVL_NAME_TECHINICAL: logging.DEBUG - 1,
    LVL_NAME_DETAILED: logging.DEBUG + 1,
    LVL_NAME_INFORMATIVE: logging.INFO - 1,
    LVL_NAME_OVERALL: logging.INFO,
    LVL_NAME_WARNING: logging.WARNING,
    LVL_NAME_ERROR: logging.ERROR
}

# default logging level
DEFAULT_LOG_LVL_NAME = LVL_NAME_OVERALL

# Mapping of logging level for each verbocity for the CONSOLE handler
CONSOLE_LEVELS = {
    TRACING_VERBOCITY: LVL_NAME_DETAILED,
    VERBOSE_VERBOCITY: LVL_NAME_INFORMATIVE,
    NORMAL_VERBOCITY: LVL_NAME_OVERALL,
    QUIET_VERBOCITY: LVL_NAME_WARNING,
}

# Mapping of lLogging level for each verbocity for the FILE handler
FILE_LEVELS = {
    TRACING_VERBOCITY: LVL_NAME_TECHINICAL,
    VERBOSE_VERBOCITY: LVL_NAME_TECHINICAL,
    NORMAL_VERBOCITY: LVL_NAME_DETAILED,
    QUIET_VERBOCITY: LVL_NAME_OVERALL,
}

# logfile path
LOG_FILE = 'pyebasy.log'

########################################################################################################################


def _construct_console_handler() -> logging.StreamHandler:
    """ Constructs the console handler. """
    console_handler = logging.StreamHandler()

    level = LEVELS[DEFAULT_LOG_LVL_NAME]
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_formatter)
    return console_handler


def _construct_file_handler() -> logging.FileHandler:
    """ Constructs the file handler. """
    file_handler = logging.FileHandler(LOG_FILE)

    level = LEVELS[DEFAULT_LOG_LVL_NAME]
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)12s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    return file_handler


def construct_logger() -> Tuple[logging.Logger, logging.StreamHandler, logging.FileHandler]:
    """ Constructs the actual logger with the handlers. """
    logger = logging.getLogger("pyebasy")

    # console logging
    console_handler = _construct_console_handler()
    logger.addHandler(console_handler)

    # logfile logging
    file_handler = _construct_file_handler()
    logger.addHandler(file_handler)

    for level_name, level_value in LEVELS.items():
        logging.addLevelName(level_value, level_name)

    return logger, console_handler, file_handler

########################################################################################################################


def set_verbocity(verbocity: Literal['tracing', 'debug', 'normal', 'quiet']):
    """ Changes the verbocity level (changes the registered logger levels) """

    console_level = LEVELS[CONSOLE_LEVELS[verbocity]]
    file_level = LEVELS[FILE_LEVELS[verbocity]]
    logger_level = min(console_level, file_level)

    _logger.setLevel(logger_level)
    _console_handler.setLevel(console_level)
    _file_handler.setLevel(file_level)


########################################################################################################################

# The actual logger and handlers (internals)
_logger, _console_handler, _file_handler = construct_logger()

########################################################################################################################


def log_technical(msg: str):
    """ Logs the technical message, usually low-level technical or raw external data. """
    level = LEVELS[LVL_NAME_TECHINICAL]
    _logger.log(level, "   " + msg)


def log_detailed(msg: str):
    """ Logs the detailed message, usually details about a single task. """
    level = LEVELS[LVL_NAME_DETAILED]
    _logger.log(level, "  " + msg)


def log_informative(msg: str):
    """ Logs the informative message, a more detailed explanation for the overall. """
    level = LEVELS[LVL_NAME_INFORMATIVE]
    _logger.log(level, " " + msg)


def log_overall(msg: str):
    """ Logs the overall message, a quick overall message about the current status. """
    level = LEVELS[LVL_NAME_OVERALL]
    _logger.log(level, msg)


def log_warning(msg: str, *args, **kwargs):
    """ Logs the warning message. """
    level = LEVELS[LVL_NAME_WARNING]
    _logger.log(level, msg, *args, **kwargs)


def log_error(msg: str, *args, **kwargs):
    """ Logs the error message. """
    level = LEVELS[LVL_NAME_ERROR]
    _logger.log(level, msg, *args, **kwargs)


########################################################################################################################
