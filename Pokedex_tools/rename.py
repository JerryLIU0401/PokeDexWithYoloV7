# -*- coding: utf-8 -*-
"""
Created on Sun May 28 03:14:06 2023

@author: jerry
"""

import os
import shutil

def rename_files(directory, prefix):
    file_list = os.listdir(directory)  # 取得目錄下的所有檔案列表
    #jpg_files = [f for f in file_list if f.endswith(".jpg")]  # 過濾出jpg檔案

    for i, filename in enumerate(file_list):
        if filename.endswith("jpg") or filename.endswith(".jpeg") or filename.endswith(".webp") or filename.endswith(".png") or filename.endswith(".gif") or filename.endswith(".avif"):
            new_filename = prefix + str(i).zfill(4) + ".jpg"  # 新的檔案名稱
            old_path = os.path.join(directory, filename)  # 原始檔案的完整路徑
            new_path = os.path.join(directory, new_filename)  # 新檔案的完整路徑
            shutil.move(old_path, new_path)  # 改變檔案名稱
    
            print(f"Renamed '{filename}' to '{new_filename}'.")

# 測試程式碼
directory_path ="D:\PokemonData\Pokedex\Wartortle"  # 目錄路徑
new_prefix = "Wartortle"  # 新的檔案名稱前綴

current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)

rename_files(directory_path, new_prefix)
# rename_files(directory_path, folder_name)
