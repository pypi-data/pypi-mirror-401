import logging
from pathlib import Path


def get_hook_logger(name="TaskHook"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    home = Path.home()

    log_dir = home / ".task" / "hooks" / "log"

    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s"
    )

    fh_err = logging.FileHandler(log_dir / "error.log", encoding="utf-8")
    fh_err.setLevel(logging.ERROR)
    fh_err.setFormatter(formatter)

    fh_run = logging.FileHandler(log_dir / "run.log", encoding="utf-8")
    fh_run.setLevel(logging.DEBUG)
    fh_run.setFormatter(formatter)

    logger.addHandler(fh_err)
    logger.addHandler(fh_run)

    return logger
