import os
res = []
dir_path = "assets/content"
for (dir_path, dir_names, file_names) in os.walk(dir_path):
    res.append((dir_path, dir_names, file_names))
print(res)
