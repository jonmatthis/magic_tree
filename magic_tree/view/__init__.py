import logging

# set up logging
from magic_tree.system.configure_logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)
