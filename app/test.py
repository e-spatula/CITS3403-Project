import os
file_list = []
for root, dirs, files in os.walk("."):
    file_list.append(files)

print(file_list)
    