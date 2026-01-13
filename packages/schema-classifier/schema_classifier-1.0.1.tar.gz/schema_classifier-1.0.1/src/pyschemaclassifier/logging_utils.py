
"""Colored logs & JSON logs (MVP skeleton)."""
import logging

def setup_logging(json_logs: bool = False, verbosity: int = 0):
    level = logging.INFO
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.WARNING
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')
