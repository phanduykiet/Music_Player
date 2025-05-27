from tkinter import *
from mutagen.mp3 import MP3
import time
import pygame
from tkinter.font import Font
import os
import tkinter.ttk as ttk
from collections import namedtuple

# tạo kiểu dữ liệu pair
Pair = namedtuple('Pair', ['first', 'second'])

# Tạo một node trong danh sách liên kết đôi
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# Danh sách liên kết đôi
class DoubleLinkedList:
    # tu dong tao khi goi class()
    def __init__(self):
        self.head = None
        self.tail = None
    # xoa toan bo
    def clear(self):
        self.head = None
        self.tail = None
    # xoa 1 phan tu
    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev
        node.next = None
        node.prev = None  
    # tìm kiếm 1 phần tử
    def search(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = self.head
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            self.tail = new_node

    def get_next(self, current_node):
        return current_node.next

    def get_prev(self, current_node):
        return current_node.prev

# Môt album có kiểu dữ liệu là danh sách liên kết đôi
class music_player:
    # tu dong tao khi gọi class()
    def __init__(self):
        self.playlist = DoubleLinkedList()
        self.current_song_node = None  
    # xoa
    def clear_playlist(self):
        self.playlist.clear()
        self.current_song_node = None

# Kiểm tra bài hát có nằm trong danh sách yêu thích
def check_Favorite(favorite, current_song):
    for song in favorite:
        if song == current_song:
            return True
    return False

# Thêm bài hát từ foder vào các album
def Make_album(us_uk, chill, kpop, pop, home, root):
    root.directory = ('Album')
    i = 0
    for song in os.listdir(root.directory):
        string = song[:3]
        home.playlist.append(song)
        if string == "Chi":
            chill.playlist.append(song)
        else:
            if string == "Pop":
                pop.playlist.append(song)
            else:
                if string == "Kpo":
                    kpop.playlist.append(song)
                else:
                    if string == "Us-":
                        us_uk.playlist.append(song)
        i = i + 1

# tìm kiếm bài hát trong main
def check_song_main(music, main):
    i = 0
    max = 0
    b = 0
    current = main.playlist.head
    while current is not None:
        cont = 0
        for char in set(music.upper()):
            if char in current.data.upper():
                cont = music.upper().count(char) + cont
        if cont > max:
            max = cont
            b = i
        i = i + 1
        current = current.next
    return b

# Tìm kiếm album
def check_search_album(type, music):
    for album in type.keys():
        if music.upper() == album.upper():
            return True
    return False

# Thanh tăng giảm âm lượng
def set_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)

# Canh giữa khung hình
def make_center(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Tính toán vị trí cửa sổ
    x_coordinate = int((screen_width / 2) - (815 / 2))
    y_coordinate = int((screen_height / 2) - (550 / 2))
    # Đặt vị trí cửa sổ
    root.geometry(f"815x550+{x_coordinate}+{y_coordinate}")
def create_center(create_playlist):
    screen_width = create_playlist.winfo_screenwidth()
    screen_height = create_playlist.winfo_screenheight()
    # Tính toán vị trí cửa sổ
    x_coordinate = int((screen_width / 2) - (400 / 2))
    y_coordinate = int((screen_height / 2) - (200 / 2))
    # Đặt vị trí cửa sổ
    create_playlist.geometry(f"400x200+{x_coordinate}+{y_coordinate}")
def save_center(save):
    screen_width = save.winfo_screenwidth()
    screen_height = save.winfo_screenheight()
    # Tính toán vị trí cửa sổ
    x_coordinate = int((screen_width / 2) - (300 / 2))
    y_coordinate = int((screen_height / 2) - (200 / 2))
    # Đặt vị trí cửa sổ
    save.geometry(f"300x200+{x_coordinate}+{y_coordinate}")