from pathlib import Path
from typing import Union, Iterable, Callable

from magic_tree import logger
from magic_tree.magic_tree_dictionary import MagicTreeDictionary


def load_directory(self, directory: str) -> None:
    """
    Load all the paths and subpaths inside the given directory to the tree.
    """
    base_path = Path(directory)
    for path in base_path.rglob('*'):
        if path.is_file():
            relative_path = path.relative_to(base_path)
            self[relative_path.parts] = path.name

    return self


def load_directory(root_directory: str,
                   tree: MagicTreeDictionary = MagicTreeDictionary(),
                   recursion_depth: int = -1,
                   included_extensions: Union[str, Iterable[str]] = None,
                   excluded_extensions: Union[str, Iterable[str]] = None,
                   include_hidden_files: bool = False,
                   included_directories: Union[str, Iterable[str]] = None,
                   excluded_directories: Union[str, Iterable[str]] = None,
                   included_file_names: Union[str, Iterable[str]] = None,
                   excluded_file_names: Union[str, Iterable[str]] = None,
                   content_loader: Callable = None) -> MagicTreeDictionary:
    """
    Load the paths and files of the input `directory` into the tree using pathlib.Path.rglob.

    Loads all found paths and files as nodes of the tree, e.g. tree['root']['path']['to']['file.txt']   = {'path': str(Path('root/path/to/file.txt')),
                                                                                                        'content': content_loader(Path('root/path/to/file.txt')) if content_loader is not None else None

    :param recursion_depth: The depth to recurse into the directory. -1 is infinite.
    :param included_extensions: A string or list of strings of file extensions to include (e.g. 'txt' or ['txt', 'csv']) if None, all files are included.
    :param excluded_extensions: A string or list of strings of file extensions to exclude (e.g. 'txt' or ['txt', 'csv']) if None, no files are excluded.
    :param include_hidden_files: Whether to include hidden files (files that start with a '.')
    :param included_directories: A string or list of strings of directory names to include (e.g. 'data' or ['data', 'logs']) if None, all directories are included.
    :param excluded_directories: A string or list of strings of directory names to exclude (e.g. 'data' or ['data', 'logs']) if None, no directories are excluded.
    :param content_loader: If defined, we will call this function on each file we find, and use the return value as the value for that file in the tree. If none, just inlude the path.
    """

    if included_extensions is None:
        included_extensions = []
    elif isinstance(included_extensions, str):
        included_extensions = [included_extensions]
    if excluded_extensions is None:
        excluded_extensions = []
    elif isinstance(excluded_extensions, str):
        excluded_extensions = [excluded_extensions]
    if included_directories is None:
        included_directories = []
    elif isinstance(included_directories, str):
        included_directories = [included_directories]
    if excluded_directories is None:
        excluded_directories = []
    elif isinstance(excluded_directories, str):
        excluded_directories = [excluded_directories]

    root_directory = Path(root_directory)

    if not root_directory.exists():
        raise FileNotFoundError(f"Directory {root_directory} does not exist.")

    if not root_directory.is_dir():
        root_directory = root_directory.parent

    for path in root_directory.rglob("*"):
        if path.is_dir() and recursion_depth != 0:
            if not include_hidden_files and path.name.startswith('.'):
                continue
            if path.name in excluded_directories:
                continue
            if included_directories and path.name not in included_directories:
                continue

            if content_loader is not None:
                try:
                    content = content_loader(path)
                except Exception as e:
                    logger.error(f"Error loading content from {path}.")
                    logger.exception(e)
                    content = None
            else:
                content = None
            tree_path = path.relative_to(root_directory).parts
            tree[path.relative_to(root_directory).parts] = {'path': path,
                                                       'content': content}
        else:
            if not include_hidden_files and path.name.startswith('.'):
                continue
            if path.suffix in excluded_extensions:
                continue
            if included_extensions and path.suffix not in included_extensions:
                continue
            try:
                content = content_loader(path) if content_loader is not None else None
            except Exception as e:
                logger.error(f"Error loading content from {path}.")
                logger.exception(e)
                content = None
            tree[path.name] = {'path': path,
                               'content': content_loader(path) if content_loader is not None else None}

    return tree


if __name__ == "__main__":
    tree = load_directory(root_directory=str(Path(__file__).parent.parent),
                          recursion_depth=1,
                          included_extensions=['py'],
                          excluded_file_names=["poetry.lock", ".gitignore", "LICENSE", "*.env"],
                          included_file_names=["*.py"],
                          included_directories=["magic_tree"],
                          excluded_directories=["__pycache__", ".git", "legacy", ".idea", "venv", ".pytest_cache"],
                          content_loader=lambda x: x.read_text())
    print(tree)
