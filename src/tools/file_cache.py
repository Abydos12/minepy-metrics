import json
import logging
import os
from time import time
from typing import Dict

from nbt import nbt


class BaseFileCache:
    _cache_content: Dict = dict()
    _cache_last_update: Dict = dict()

    def __getitem__(self, item):
        if (
                item not in self._cache_last_update
                or os.stat(item).st_mtime > self._cache_last_update[item]
        ):
            return self.__missing__(item)
        return self._cache_content[item]

    def __setitem__(self, key, value):
        self._cache_last_update[key] = time()
        self._cache_content[key] = value

    def __missing__(self, key):
        with open(key, "r") as fd:
            value = [line for line in fd.readlines()]
            self[key] = value
            return value


class JsonFileCache(BaseFileCache):
    def __missing__(self, key):
        try:
            with open(key, "r") as fd:
                value = json.load(fd)
                self[key] = value
                return value
        except FileNotFoundError:
            logging.error(f"File [{key}] not found")


class NbtFileCache(BaseFileCache):
    def __missing__(self, key):
        try:
            value = nbt.NBTFile(key, "rb")
            self[key] = value
            return value
        except FileNotFoundError:
            logging.error(f"File [{key}] not found")
