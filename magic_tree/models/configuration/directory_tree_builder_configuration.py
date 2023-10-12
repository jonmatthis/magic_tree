from typing import List, Callable

from pydantic import BaseModel, Field


class DirectoryTreeConfig(BaseModel):
    included: List[str] = Field(default=[], description="List of files/folders to include, e.g. ['data', 'logs']")
    excluded: List[str] = Field(default=['__pycache__', '.git', '*env', '*.pyc', '*.pyo', '*.pyd', '.DS_Store'],
                                description="List of files/folders to exclude, e.g. ['__pycache__', '.git', 'env']")
    recursion_depth: int = Field(
        0,
        description="0 means it won't go into subdirectories, -1 means it will go into all subdirectories",
    )
    file_opener: Callable = Field(default=lambda path: open(path, "r", encoding="utf-8"),
                                  description="Function to open files with")
