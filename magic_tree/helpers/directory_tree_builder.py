from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, Hashable, Union

from pydantic import BaseModel, root_validator

from magic_tree import logger
from magic_tree.magic_tree_dictionary import MagicTreeDictionary
from magic_tree.models.configuration.directory_tree_builder_configuration import DirectoryTreeConfig


class DirectoryTreeBuilder(BaseModel):
    root_path: Path
    config: DirectoryTreeConfig
    tree: MagicTreeDictionary

    @root_validator
    def validate_root_path(cls, values):
        root_path = values["root_path"]

        if not Path(root_path).is_dir():
            raise ValueError(f"root_path {root_path} is not a directory")
        return values

    @classmethod
    def from_path(cls,
                  path: Union[Path, str],
                  config: DirectoryTreeConfig = None,
                  tree=None,
                  create_directory: bool = False):
        if create_directory:
            Path(path).mkdir(parents=True, exist_ok=True)
        if tree is None:
            tree = MagicTreeDictionary()
        if config is None:
            config = DirectoryTreeConfig()

        instance = cls(root_path=path,
                       config=config,
                       tree=tree)

        instance.fetch_file_content(path)
        return instance

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
        tree_path = [f"{Path(self.root_path).stem}/"]
        path = Path(path)
        if path == self.root_path:
            return tree_path

        path = Path(path)

        path_paths = path.relative_to(Path(self.root_path)).parts
        tree_path.extend([f"{path}/" for part in path_paths if part not in self.config.excluded])
        return tree_path


if __name__ == "__main__":
    root_directory_in = r"C:\Users\jonma\github_repos\jonmatthis\magic_tree\magic_tree"
    directory_tree = DirectoryTreeBuilder.from_path(path=root_directory_in)

    print(directory_tree.tree)
