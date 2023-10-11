import logging

from magic_tree.helpers.demo import magic_tree_demo
from magic_tree.magic_tree_dict import MagicTreeDict

# Alternative names
MagicTree = MagicTreeDict
demo = magic_tree_demo

# set up logging
from magic_tree.system.configure_logging import configure_logging

configure_logging()

