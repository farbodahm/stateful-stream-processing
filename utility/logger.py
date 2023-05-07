import logging


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    normal_format = "%(levelname)s: %(asctime)s - %(message)s"
    verbose_format = (
        "%(levelname)s: %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + verbose_format + reset,
        logging.INFO: grey + normal_format + reset,
        logging.WARNING: yellow + verbose_format + reset,
        logging.ERROR: red + verbose_format + reset,
        logging.CRITICAL: bold_red + verbose_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# logging.basicConfig(format="%(levelname)s: %(asctime)s - %(message)s", level=logging.INFO)

logger = logging.getLogger("Stateful-Stream-Processing")
logger.setLevel(logging.INFO)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
