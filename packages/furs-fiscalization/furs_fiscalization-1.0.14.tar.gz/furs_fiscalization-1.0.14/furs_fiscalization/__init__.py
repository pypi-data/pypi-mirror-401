import logging

from .logging_utils import configure_logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Optional env-driven setup (safe under Odoo; does nothing unless env vars are set).
configure_logging()


