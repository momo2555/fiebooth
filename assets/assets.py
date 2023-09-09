import os
from errors.errors import AssetsNotFoundException

def get_asset_uri(file_name) -> str:
    dir_path = "assets/content"
    for (dir_path, dir_names, file_names) in os.walk(dir_path):
        if file_name in file_names:
            return f"{dir_path}/{file_name}"
    raise AssetsNotFoundException
