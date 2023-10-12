import logging

from magic_tree.demo import magic_tree_demo as demo
from magic_tree.magic_tree_dictionary import MagicTreeDictionary as MagicTree
# set up logging
from magic_tree.system.configure_logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)
