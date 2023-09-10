import os
from glob import glob

res = []
dir_path = "assets/content"
for (dir_path, dir_names, file_names) in os.walk(dir_path):
    res.append((dir_path, dir_names, file_names))
print(res)


test = glob("/home/fiebooth/.fiebooth/photos/*/", recursive = False)
print(test)
