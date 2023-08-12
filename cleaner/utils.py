import os
from re import search, IGNORECASE
from paths import (
    USER_TEMP_DIR,
    SYSTEM_TEMP_DIR,
    PREFETCH_DIR,
    LOCAL_DIR,
)


def get_dir_size(dir_path: str) -> int:
    """
    Return size of the directory in bytes.

    :param dir_path: Path of directory
    :type dir_path: str
    :return: Size of the directory in bytes
    :rtype: int
    """
    size = 0

    for root, _, files in os.walk(dir_path):
        size += sum(os.path.getsize(os.path.join(root, name)) for name in files)

    return size


def get_dirs_size(dir_paths: list) -> int:
    """
    Return size of a list of directories.

    :param dir_paths: List of directory paths
    :type dir_paths: list
    :return: Size of directories in dir_paths
    :rtype: intyield
    """
    size = 0

    for dir in dir_paths:
        size += get_dir_size(dir)

    return size


def get_formatted_size(size: int) -> str:
    """
    Return size in KB's, MB's or GB's.

    :param size: Size in bytes
    :type size: int
    :return: Size in KB's, MB's or GB's.
    :rtype: str
    """
    size /= 1024
    suffixes = ["KB", "MB", "GB"]

    for suffix in suffixes:
        if size < 1024:
            break
        size /= 1024

    return f"{size:.2f}{suffix}"


def get_cache_dirs():
    """Yields a list of name and path of cache dirs."""

    cache_dirs = set()
    for root, _, _ in os.walk(LOCAL_DIR):
        if matches := search(
            r"(.+local\\(\w+)\\((?:.+)\\)?(?:cache2?))\\", root, IGNORECASE
        ):
            dir = matches.group(1)
            name = matches.group(2)
            if dir not in cache_dirs:
                yield [f"{name.title()}\nCache", dir]
            cache_dirs.add(dir)

    yield ["User\nTemp", USER_TEMP_DIR]
    yield ["System\nTemp", SYSTEM_TEMP_DIR]
    yield ["Prefetch", PREFETCH_DIR]
