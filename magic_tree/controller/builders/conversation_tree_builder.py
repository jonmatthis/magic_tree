import logging
from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, Hashable, Union

from magic_tree.magic_tree_dictionary import MagicTreeDictionary
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ConversationTreeBuilder(BaseModel):
    chats: Dict[str, Any]
    tree: MagicTreeDictionary

    @classmethod
    def from_chats(cls,
                   chats: Dict[str, Any],
                   ) -> 'MagicTreeDictionary':

        tree = MagicTreeDictionary()
        for chat in chats:
            context_route = [chat.server_name, chat.channel_name, chat.thread_name]

        instance = cls(chats=chats,
                       config=config,
                       tree=tree)

        return tree

    def fetch_file_content(self, path: Union[str, Path], current_depth=0) -> 'MagicTreeDictionary':
        logger.trace(f"Fetching content for path: {path}")
        path = Path(path)
        for path in Path(path).rglob("*"):
            if path.is_file() and self.should_include_path(path):
                tree_path = self._convert_to_tree_path(path=path)
                self.tree[tree_path] = {"type": "file",
                                        "content": {"file_name": path.name,
                                                    "file_type": path.suffix,
                                                    "file_stats": {"bytes": path.stat().st_size,
                                                                   "last_modified_utc": path.stat().st_mtime,
                                                                   "last_accessed_utc": path.stat().st_atime,
                                                                   "created_utc": path.stat().st_ctime,
                                                                   },
                                                    "content": self._get_file_content(file_path=path)}}
        return self.tree

    def should_include_path(self, path: Path) -> bool:
        filename = path.name
        for pattern in self.config.excluded:
            if fnmatch(filename, pattern):
                return False

        if not self.config.included:
            return True

        for pattern in self.config.included:
            if fnmatch(filename, pattern):
                return True
        return False

    @staticmethod
    def _get_file_content(file_path: Union[str, Path]) -> str:
        logger.trace(f"Getting content for file: {file_path}")

        try:
            content = open(file_path, "r", encoding="utf-8").read()
            if not content:
                content = "<empty file>"
            return content
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return "<content could not be loaded>"

    def _convert_to_tree_path(self, path: Union[str, Path]) -> Iterable[Hashable]:
        tree_path = []
        path = Path(path)
        if path == self.root_path:
            return tree_path

        path = Path(path)

        path_parts = path.relative_to(Path(self.root_path)).parts
        for part in path_parts:
            if not "." in part:
                tree_path.append(f"{part}/")
            else:
                tree_path.append(part)

        return tree_path


if __name__ == "__main__":
    root_directory_in = r"C:\Users\jonma\github_repos\jonmatthis\magic_tree\magic_tree"
    directory_tree = DirectoryTreeBuilder.from_path(path=root_directory_in)

    directory_tree.print()
