import os
import json


class CacheData:
    def __init__(self, id: int, version: int, content: tuple):
        self.meta = {
            "id": id,
            "version": version
        }
        self.content = content


class Cache:
    PATH = "/cache/"
    PATH_META = PATH + "_meta_.json"

    def __init__(self):
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)

        if os.path.isfile(self.PATH_META):
            with open(self.PATH_META, "r", encoding="utf-8") as f:
                self.cache_meta = json.load(f)
        else:
            self.cache_meta = {}

        self.loaded_data = {}

    def add_data(self, data: CacheData):
        meta = data.meta
        if meta.id not in self.cache_meta:
            self.cache_meta[meta.id] = []

        vid = self._get_vid(data)
        if meta.version not in self.cache_meta[meta.id]:
            self.cache_meta[meta.id].append(meta)
            self.save_data(data)

        if vid not in self.loaded_data:
            self.loaded_data[vid] = data.content

    def save_meta(self):
        with open(self.PATH_META, "w", encoding="utf-8") as f:
            json.dump(self.cache_meta, f, ensure_ascii=False)

    def save_data(self, data: CacheData):
        vid = self._get_vid(data)
        path = self.PATH + vid + ".json"

        with open(path, "w", encoding='utf-8') as f:
            json.dump(data.content, f, ensure_ascii=False)

    def load_data(self, vid: str):
        path = self.PATH + vid + ".json"

        if os.path.isfile(path):
            with open(path, "r", encoding='utf-8') as f:
                self.loaded_data[vid] = json.load(f)
        else:
            print("The path:", path, "is not a valid data file")

    def unload_data(self):
        self.loaded_data = {}

    def clear_cache(self):
        self.cache_meta = {}
        self.loaded_data = {}

        files = os.scandir(self.PATH)
        for f in files:
            os.remove(f.path)

    def _get_vid(self, data: CacheData):
        return str(data.meta.id) + "-" + str(data.meta.version)
