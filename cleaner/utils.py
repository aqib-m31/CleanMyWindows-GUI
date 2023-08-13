import os
from re import search, IGNORECASE
from .paths import USER_TEMP_DIR, SYSTEM_TEMP_DIR, LOCAL_DIR
from shutil import rmtree


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


def clean_dir(dir: str) -> list:
    """
    Clean a directory.

    :param dir: Path of a directory
    :type dir: str
    :return: List of Cleaned size and No. of files that couldn't be deleted
    :rtype: list
    """
    cleaned_size = 0
    access_denied_files = 0

    if not os.path.exists(dir):
        return [0, 0]
    
    try:
        files = os.listdir(dir)

        if not files:
            return cleaned_size

        for file in files:
            path = os.path.join(dir, file)
            try:
                if not os.path.isdir(path):
                    file_size = os.path.getsize(path)
                    os.remove(path)
                else:
                    file_size = get_dir_size(path)
                    rmtree(path)
            except PermissionError:
                access_denied_files += 1
                continue
            else:
                cleaned_size += file_size
    except PermissionError:
        access_denied_files += 1

    return [cleaned_size, access_denied_files]
