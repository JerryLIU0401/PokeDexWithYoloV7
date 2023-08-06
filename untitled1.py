# -*- coding: utf-8 -*-
"""
Created on Sat May 27 03:09:59 2023

@author: jerry
"""

import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage
from PIL import ImageTk, Image
import numpy as np
import cv2
import shutil
import subprocess
import webbrowser
import re
# from yolov7.detect import getImageDetectAfter

root = tk.Tk()
# weights_path = "Pokedex.dataset/best.pt"
imagePath = "Pokedex.dataset/test/images"
command = [
        "python",
        "detect.py",
        "--weights",
        "Pokedex.dataset/best.pt",
        "--conf",
        "0.25",
        "--img-size",
        "640",
        "--source",
        imagePath
    ]
url = ""
pokemonResult = []
selectRec = []
origin_img = []
RED = (0, 0, 255) # BGR

def open_image():
    global imagePath, command, url, origin_img
    # 打開檔案對話框，讓使用者選擇圖片
    file_path = filedialog.askopenfilename()
    #reset data
    pokemonResult.clear()
    selectRec.clear()
    origin_img.clear()
    
    # 如果使用者選擇了圖片檔案
    if file_path:
        # file_path = file_path.encode('utf-8').decode('utf-8')
        imagePath = file_path
        command[-1] = imagePath
        print(command)
        subprocess.run(command)
        readData()
        image_denoised = cv2.fastNlMeansDenoisingColored(cv2.imread("./result/result.jpg"), None, 10, 10, 7, 21)
        origin_img = image_denoised
        selectPokemon()
        # cv2.rectangle(image_denoised, selectRec[0], selectRec[1], red_color, 3, cv2.LINE_AA)
        
        # image = Image.fromarray(cv2.cvtColor(image_denoised, cv2.COLOR_BGR2RGB))
        
        # # 等比例縮小圖片
        # width, height = image.size
        # max_width = 400
        # max_height = 300
        # aspect_ratio = min(max_width / width, max_height / height)
        # new_width = int(width * aspect_ratio)
        # new_height = int(height * aspect_ratio)
        # image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # # 建立 ImageTk 物件
        # image_tk = ImageTk.PhotoImage(image)
        # label.configure(image=image_tk)
        # label.image = image_tk

        

def readData():
    global btnName, url, root, selectRec
    filename = "./result/imagedata.txt"
    pattern = r'\d+' # 正則表達式模式，匹配一個或多個數字
    with open(filename, "r") as file:
        lines = file.readlines()
        # text = file.read()
    for index, line in enumerate(lines, start=1):
            if "$" in line:   #找到$的那一行 
                result = lines[index-6]
                pokemonResult.append(onlyAlpha(result))
                setPokemonData(0)
            matches = re.findall(pattern, line)
            selectRec.extend(matches)
    
index = 0
def setPokemonData(index):
    global url
    if len(pokemonResult) != 0:
        # print(pokemonResult)
        pokemon_name = pokemonResult[index].strip()
        # print(pokemon_name)
        btnName.config(text = "名稱: " + translate[pokemon_name][0])
        btnAttributes.config(text = "屬性: " + translate[pokemon_name][1])
        btnId.config(text = "編號: " + translate[pokemon_name][2])
        url = translate[pokemon_name][3]
        root.update()


def goToNextPage():
    global index
    if len(pokemonResult) != 0:
        if index == len(pokemonResult) - 1:
            pass
        else:
            index+=1
            setPokemonData(index)
            selectPokemon()
            
def goToPreviousPage():
    global index
    if len(pokemonResult) != 0:
        if index == 0:
            pass
        else:
            index-=1
            setPokemonData(index)
            selectPokemon()
        
def onlyAlpha(text):
    name = ''
    for i in range(len(text)):
        if text[i].isalpha():
            name = name + text[i]
    return name

def openURL():
    global url
    # url = "https://tw.portal-pokemon.com/play/pokedex/0063"
    webbrowser.open(url)
    # print("open")
    
def selectPokemon():
    global selectRec, index, origin_img
    position = [selectRec[i:i+4] for i in range(0, len(selectRec), 4)]
    img = origin_img.copy()
    # cv2.imshow("", origin_img)
    cv2.rectangle(img, (int(position[index][0]), int(position[index][1])), (int(position[index][2]), int(position[index][3])), RED, 2, cv2.LINE_AA)
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # 等比例縮小圖片
    width, height = image.size
    max_width = 400
    max_height = 300
    aspect_ratio = min(max_width / width, max_height / height)
    new_width = int(width * aspect_ratio)
    new_height = int(height * aspect_ratio)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 建立 ImageTk 物件
    image_tk = ImageTk.PhotoImage(image)
    label.configure(image=image_tk)
    label.image = image_tk
    
    root.update()
    

   
# def typeIcon(pokemontype):
#     global root
#     if(pokemontype == "草系"):
#         # print("t")
#         image = PhotoImage(file="C:/Users/jerry/OneDrive/Desktop/Pokedex/yolov7/type/grass.png")
#         # image = image.subsample(5, 5) 
#         button = tk.Button(root, image=image)
#         button.place(x=350, y=650) 
#         return image
    
        
translate = {'Abra':["凱西", "超能系", "0063", "https://wiki.52poke.com/wiki/%E5%87%AF%E8%A5%BF"], 
             'Kadabra': ['勇吉拉', "超能系", "0064", "https://wiki.52poke.com/wiki/%E5%8B%87%E5%9F%BA%E6%8B%89"] , 
             'Alakazam' : ['胡地', "超能系", "0065", "https://wiki.52poke.com/wiki/%E8%83%A1%E5%9C%B0"], 
             'Charmander': ['小火龍', "火系", "0004", "https://wiki.52poke.com/wiki/%E5%B0%8F%E7%81%AB%E9%BE%99"] , 
             'Charmelon': ['火恐龍', "火系", "0005", "https://wiki.52poke.com/wiki/%E7%81%AB%E6%81%90%E9%BE%99"], 
             'Charizard': ['噴火龍',"火系", "0006", "https://wiki.52poke.com/wiki/%E5%96%B7%E7%81%AB%E9%BE%99"],
             'Squirtle': ['傑尼龜', "水系", "0007", "https://wiki.52poke.com/wiki/%E6%9D%B0%E5%B0%BC%E9%BE%9F"], 
             'Watortle': ['卡咪龜', "水系", "0008", "https://wiki.52poke.com/wiki/%E5%8D%A1%E5%92%AA%E9%BE%9F"], 
             'Blastoise': ['水箭龜', "水系", "0009", "https://wiki.52poke.com/wiki/%E6%B0%B4%E7%AE%AD%E9%BE%9F"],
             'Bulbasaur': ['妙蛙種子', "草系", "0001", "https://wiki.52poke.com/wiki/%E5%A6%99%E8%9B%99%E7%A7%8D%E5%AD%90"], 
             'Ivysaur': ['妙蛙草', "草系", "0002", "https://wiki.52poke.com/wiki/%E5%A6%99%E8%9B%99%E8%8D%89"], 
             'Venusaur': ['妙蛙花', "草系", "0003", "https://wiki.52poke.com/wiki/%E5%A6%99%E8%9B%99%E8%8A%B1"]}

root.title("Pokedex")
root.iconbitmap("icon.ico")

window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

frame_width = 500
frame_height = 800

left = int((window_width - frame_width)/2)
top = int((window_height - frame_height)/2)

root.geometry(f'{frame_width}x{frame_height}+{left}+{top}')

# ttk.Style().configure("TButton", background="#FFFAFA", relief="flat")
style = ttk.Style()
style.theme_use('alt')
style.map('TButton', background=[('active', '#ff0000')])
style.theme_create( "button-center", settings={
        "TButton": {"configure": {"anchor": "center"}}} )

nameBtnStyle = ttk.Style()

style.configure("Custom.TButton", borderwidth=1, padding=6, focusthickness=2, 
                font=("Arial", 24), width=7, height=1, )


nameBtnStyle.configure("Name.TButton",font=("Arial", 24),padding=6, anchor='w', width=7, height=1)

btnDetail = ttk.Button(root, text="詳細資料", style="Custom.TButton", command=openURL)

btnDetail.place(x=330, y=450)

btnSelectImg = ttk.Button(root, text="選擇圖片", style="Custom.TButton", command=open_image)

btnSelectImg.place(x=330, y=550)

btnAttributes = ttk.Button(root, text="屬性: ", style="Name.TButton", width = 15)

btnAttributes.place(x=30, y=550)

btnName = ttk.Button(root, text="名稱: ", style="Name.TButton", width = 15)

btnName.place(x=30, y=350)

btnId = ttk.Button(root, text="編號: ", style="Name.TButton", width = 15)

btnId.place(x=30, y=450)

btnNext = ttk.Button(root, text="下一個", style="Name.TButton", command=goToNextPage)

btnNext.place(x=330, y=650)

btnPrevious = ttk.Button(root, text="上一個", style="Name.TButton", command=goToPreviousPage)

btnPrevious.place(x=30, y=650)

i = PhotoImage(file="C:/Users/jerry/OneDrive/Desktop/Pokedex/yolov7/type/grass.png")
i = i.subsample(2, 2) 

typeIcon = tk.Label(root, image=i, width=100, height=100)
typeIcon.place(x=320, y=320) 

typeIcon2 = tk.Label(root, image=i, width=100, height=100)
typeIcon2.place(x=405, y=320)  

# 建立 Label 並顯示圖片
label = tk.Label(root, compound=tk.CENTER)
label.place(x=30,y=30)


root.mainloop()