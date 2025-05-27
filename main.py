from functions import*
import tkinter as tk
from tkinter import *
from mutagen.mp3 import MP3
import time
import pygame
from tkinter.font import Font
import os
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime

# Khởi tạo window
root = Tk()
root.title('Music Player')
root.geometry("815x550")
root.resizable(0,0)
make_center(root)
root.grid_columnconfigure(1, minsize=300)

# Cho phép nhạc chạy
pygame.mixer.init()

# Tạo kiểu pair
Pair = namedtuple('Pair', ['first', 'second'])

# Khai báo biến toàn cục
album_music = {"home":Pair("Home",music_player()), "favorite":Pair("Favorite",music_player()), "pop":Pair("Pop", music_player()), "chill":Pair("Chill",music_player()), "us_uk":Pair("Us_Uk", music_player()), "kpop":Pair("Kpop", music_player())}
songs = []
is_running = False
temp_Pause = False
temp_Restart = False
temp_play = False
check_start = False
volume_check = False
album = "home"
music = ""
myFont = Font(family="Arial", size=14, weight="bold")
myFont1 = Font(family="Arial", size=12, weight="bold")
current_song = ""
temp_current = ""
current_time = 0
index = 0
temp_Color = 'grey'
temp_size_left = 16
temp_size_right = 14
song2list = music_player()

# Tạo một dict để lưu trữ số lần nhấn vào từng mục
trending = {}
history = []

# Tạo các album
Make_album(album_music["us_uk"].second, album_music["chill"].second, album_music["kpop"].second, album_music["pop"].second, album_music["home"].second, root)

# Chia nhỏ khung hình
frameLeft = Frame(root, borderwidth=10, relief= GROOVE, bg=temp_Color)
frameLeft.grid(row=0, column=0, ipadx=0, ipady=temp_size_left)
frameRight = Frame(root, borderwidth=10, relief= GROOVE, bg=temp_Color)
frameRight.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=temp_size_right)
songlist2 = Listbox(frameLeft, bg=temp_Color, fg="black", width=15, height=16, font=myFont1, borderwidth=0)
songlist2.grid(row=5)
frameRight0 = Frame(frameRight, bg=temp_Color)
frameRight0.grid(row=1, column=1, padx=0, pady=0, ipadx=0, ipady=0)
frameRight1 = Frame(frameRight, bg=temp_Color)
frameRight1.grid(row=2, column=1, padx=0, pady=0, ipadx=0, ipady=0)
frameRight2 = Frame(frameRight, bg=temp_Color)
frameRight2.grid(row=3, column=1, padx=0, pady=0, ipadx=0, ipady=0)
frameRight3 = Frame(frameRight, bg=temp_Color)
frameRight3.grid(row=4, column=1, padx=0, pady=0, ipadx=0, ipady=0)
frameRight4 = Frame(frameRight, bg=temp_Color)
frameRight4.grid(row=5, column=1, padx=0, pady=0, ipadx=0, ipady=0)

def on_select(event):
    global current_song
    text = label_album.cget("text")
    if album == "History" or text == "Trending":
        return
    # Lấy chỉ mục của mục được chọn
    index = songlist1.curselection()
    current_song = songlist1.get(index)
    functionRight.makeBtn_favorite()

def delete_history():
    selected_index = list_History.curselection()
    if selected_index:
        history.remove(list_History.get(selected_index))
        list_History.delete(selected_index)

# Thêm bài hát vào album mới
def click3(event):
    if album_music[songlist3.get(songlist3.curselection()[0])].second.playlist.search(current_song) != None:
        return
    else:
        temp = songlist3.get(songlist3.curselection()[0])
        album_music[temp].second.playlist.append(current_song)
    save.destroy()

# Tạo của sổ album để lưu bài hát
def save_playlist():
        global save, songlist3
        save = Tk()
        save.title("Save to playlist")
        save.geometry("300x200")
        save_center(save)
        save.resizable(0,0)
        songlist3 = Listbox(save, fg="black", width=40, height=10, font=myFont1, borderwidth=2)
        text = Label(save, text="All playlists", font=myFont1)
        text.pack(side=TOP, ipadx=97)
        songlist3.pack()
        songlist3.delete(0, END)
        for item in songlist2.get(0, END):
            songlist3.insert(END, item)
        if songlist3.size() == 0:
            return
        songlist3.bind("<<ListboxSelect>>", click3)

# Chọn bài hát
def on_double_click(event):
    global current_song, temp_play
    if songlist1.size() == 0:
        return
    current_song = songlist1.get(songlist1.curselection()[0])
    song2list.current_song_node = song2list.playlist.search(current_song)
    temp_play = False
    my_slider.set(0)
    # Lấy giá trị được chọn từ Listbox
    selected_item = songlist1.get(songlist1.curselection())
    # Lấy thời gian hiện tại
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Hiển thị lịch sử (kèm thời gian) trong Text widget
    history_listbox.insert(tk.END, f"{current_time}: {selected_item}\n")
    # Kiểm tra xem mục đã được nhấn bao nhiêu lần
    if selected_item in trending:
        trending[selected_item] += 1
    else:
        trending[selected_item] = 1
    update_trending_display()
    # Lưu lịch sử vào danh sách (hoặc biến) để theo dõi
    history.append(f"{current_time}: {selected_item}")             
    functionRight.start_music()

#  Lưu vào trending
def update_trending_display():
    global sorted_trending
    # Xóa nội dung cũ trong Listbox hiển thị số lần nhấn vào từng mục
    trending_listbox.delete(0, tk.END)
    # Sắp xếp giảm dần và hiển thị số lần nhấn vào từng mục trong Listbox
    sorted_trending = functionLeft.insertion_sort(list(trending.items()))
    for item, count in sorted_trending:
        trending_listbox.insert(tk.END, f"{item}: {count}")

# Di chuyển bằng cách kéo bài hát
def on_listbox_click(event):
    global selected_index
    selected_index = songlist1.nearest(event.y)
def on_listbox_motion(event):
    global selected_index
    if selected_index is not None:
        cur_index = songlist1.nearest(event.y)
        if cur_index != selected_index:
            item = songlist1.get(selected_index)
            songlist1.delete(selected_index)
            songlist1.insert(cur_index, item)
            selected_index = cur_index
            songlist1.selection_set(selected_index)

# Các chức năng bên trái
class functionLeft():
    # Xóa new playlist
    def delete_new_playlist():
        global album
        selected_index = songlist2.curselection()
        temp = songlist2.get(selected_index)
        del album_music[temp]
        songlist2.delete(selected_index)
        album = "home"
        functionRight.check_album()

    # Nút home
    def home():
        global album
        album = "home"
        functionRight.check_album()

    # Nút trending
    def trending():
        global sorted_trending
        if len(trending) == 0:
            return
        list_Trending.delete(0, END)
        for song, count in sorted_trending:
            list_Trending.insert("end", f"{song} : {count} lượt nghe\n")
        functionRight.makeBtn_favorite()
        label_album.configure(text="Trending", font=myFont)
        songlist1.pack_forget()
        list_History.pack_forget()
        label_album.pack_forget()
        list_Trending.pack(side=BOTTOM)
        label_album.pack(side=LEFT, pady=3)

    # Tạo album mới
    def add_playList(textbox1):
        value = textbox1.get()
        if value == "":
            return
        list_items = songlist2.get(0, END)
        for item in list_items:
            if value.lower() == item.lower():
                return
        album_music[value] = Pair(value, music_player())
        songlist2.insert("end", value)
        textbox1.configure(text="")
        create_menu.destroy()
        print(album_music[value].first)

    # Cửa sổ tạo album mới
    def add():
        global create_menu
        create_menu = Tk()
        create_menu.title('')
        create_menu.overrideredirect(True)
        create_menu.geometry("400x200")
        create_menu.resizable(0,0)
        create_menu.grid_columnconfigure(1, minsize=300)
        create_center(create_menu)
        lable_create = Label(create_menu, text="New playlist", font=myFont)
        textbox1 = Entry(create_menu, width=60)
        button1 = Button(create_menu, text="Create", font=myFont, command=lambda : functionLeft.add_playList(textbox1))
        button2 = Button(create_menu, text="Cancel", font=myFont, command=create_menu.destroy)
        lable_create.grid(row=0, pady=7)
        textbox1.grid(padx=20, row=1, pady=7)
        button1.grid(ipadx=0, row=3, pady=7)
        button2.grid(ipadx=0, row=4, pady=7)
    
    # sắp xếp theo lượt nghe
    def insertion_sort(arr):
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i-1
            while j >=0 and key[1] > arr[j][1]:
                    arr[j + 1] = arr[j]
                    j -= 1
            arr[j + 1] = key
        return arr
    
# Chức năng bên phải
class functionRight():
    # Xóa bài hát
    def delete_music():
        global index, temp_Pause, song_length, temp_song
        if songlist1.size() == 0:
            return
        my_string = ''.join(map(str, songlist1.curselection()))
        index = int(my_string)
        if index == songlist1.size() - 1:
                index = 0
        current = album_music[album].second.playlist.search(current_song)
        album_music[album].second.playlist.remove(current)
        functionRight.make_list(album_music[album].second)
        if not song2list.playlist.head:
            pygame.mixer.music.stop()
        my_slider.set(0)
        full_path = os.path.join(root.directory, current_song)
        audio = MP3(full_path)
        song_length = audio.info.length
        if temp_play == False:
            pygame.mixer.music.pause()
        else:
            functionRight.play_music()

    # Tạo menu tại nơi click
    def right_click(event):
        # Hiển thị menu tại vị trí chuột phải được nhấn
        popup_menu0.post(event.x_root, event.y_root)
    def left_click(event):
        # Hiển thị menu tại vị trí chuột trái được nhấn
        popup_menu1.post(event.x_root, event.y_root)
    def right_click_history(event):
        # Hiển thị menu tại vị trí chuột phải được nhấn
        popup_history.post(event.x_root, event.y_root)  

    # History
    def History():
        global album
        album = "history"
        functionRight.make_listHistory()
    def make_listHistory():
        global index, songs, album
        index = 0
        label_album.configure(image="", text=album.title(), font=myFont)
        list_History.delete(0, END)
        for song in history:
            list_History.insert("end", song)
        functionRight.makeBtn_favorite()
        list_Trending.pack_forget()
        songlist1.pack_forget()
        label_album.pack_forget()
        list_History.pack(side=BOTTOM)
        label_album.pack(side=LEFT, pady=3)
    
    # dark mode
    def Color():
        global temp_Color
        if temp_Color == 'grey':
            temp_Color = 'white'  
            icon_ytMusic_lable.config(bg=temp_Color)
            style.configure("TScale", background=temp_Color)
            person_lable.config(bg=temp_Color)
            frameLeft.config(bg=temp_Color)
            frameRight.config(bg=temp_Color)
            frameRight0.config(bg=temp_Color)
            frameRight1.config(bg=temp_Color)
            frameRight2.config(bg=temp_Color)
            frameRight3.config(bg=temp_Color)
            frameRight4.config(bg=temp_Color)
            home_btn.config(bg=temp_Color, activebackground=temp_Color)
            trend_btn.config(bg=temp_Color, activebackground=temp_Color)
            add_btn.config(bg=temp_Color, activebackground=temp_Color)
            pop_btn.config(bg=temp_Color, activebackground=temp_Color)
            kpop_btn.config(bg=temp_Color, activebackground=temp_Color)
            chill_btn.config(bg=temp_Color, activebackground=temp_Color)
            usuk.config(bg=temp_Color, activebackground=temp_Color)
            like_btn.config(bg=temp_Color, activebackground=temp_Color)
            label_album.config(bg=temp_Color)
            songlist1.config(bg=temp_Color)
            status_bar.config(bg=temp_Color)
            volume_btn.config(bg=temp_Color, activebackground=temp_Color)
            search_btn.config(bg=temp_Color, activebackground=temp_Color)
            next_btn.config(bg=temp_Color, activebackground=temp_Color)
            back_btn.config(bg=temp_Color, activebackground=temp_Color)
            restart_btn.config(bg=temp_Color, activebackground=temp_Color)
            favorite_btn.config(bg=temp_Color, activebackground=temp_Color)
            menu_btn.config(bg=temp_Color, activebackground=temp_Color)
            play_btn.config(bg=temp_Color, activebackground=temp_Color)
            list_History.config(bg=temp_Color)
            list_Trending.config(bg=temp_Color)
            songlist2.config(bg=temp_Color)
            slider_volume.config(bg=temp_Color, activebackground=temp_Color)
        else:
            temp_Color = 'grey'  
            style.configure("TScale", background=temp_Color)
            person_lable.config(bg=temp_Color)
            icon_ytMusic_lable.config(bg=temp_Color)
            frameLeft.config(bg=temp_Color)
            frameRight.config(bg=temp_Color)
            frameRight0.config(bg=temp_Color)
            frameRight1.config(bg=temp_Color)
            frameRight2.config(bg=temp_Color)
            frameRight3.config(bg=temp_Color)
            frameRight4.config(bg=temp_Color)
            home_btn.config(bg=temp_Color, activebackground=temp_Color)
            trend_btn.config(bg=temp_Color, activebackground=temp_Color)
            add_btn.config(bg=temp_Color, activebackground=temp_Color)
            pop_btn.config(bg=temp_Color, activebackground=temp_Color)
            kpop_btn.config(bg=temp_Color, activebackground=temp_Color)
            chill_btn.config(bg=temp_Color, activebackground=temp_Color)
            usuk.config(bg=temp_Color, activebackground=temp_Color)
            like_btn.config(bg=temp_Color, activebackground=temp_Color)
            label_album.config(bg=temp_Color)
            songlist1.config(bg=temp_Color)
            status_bar.config(bg=temp_Color)
            volume_btn.config(bg=temp_Color, activebackground=temp_Color)
            search_btn.config(bg=temp_Color, activebackground=temp_Color)
            next_btn.config(bg=temp_Color, activebackground=temp_Color)
            back_btn.config(bg=temp_Color, activebackground=temp_Color)
            restart_btn.config(bg=temp_Color, activebackground=temp_Color)
            favorite_btn.config(bg=temp_Color, activebackground=temp_Color)
            menu_btn.config(bg=temp_Color, activebackground=temp_Color)
            play_btn.config(bg=temp_Color, activebackground=temp_Color)
            list_History.config(bg=temp_Color)
            list_Trending.config(bg=temp_Color)
            songlist2.config(bg=temp_Color)
            slider_volume.config(bg=temp_Color, activebackground=temp_Color)

    # Nút favorite 
    def favorite_music():
        global current_song, index, song_length
        if songlist1.size() == 0:
            return
        x = album_music["favorite"].second.playlist.search(current_song)
        if x is not None:
            print(current_song)
            my_string = ''.join(map(str, songlist1.curselection()))
            index = int(my_string)
            if index == songlist1.size() - 1:
                index = 0
            album_music["favorite"].second.playlist.remove(x)
            if album == "favorite":
                functionRight.make_list(album_music["favorite"].second)
                if not song2list.playlist.head:
                    pygame.mixer.music.stop()
                my_slider.set(0)
                full_path = os.path.join(root.directory, current_song)
                audio = MP3(full_path)
                song_length = audio.info.length
                if temp_play == False:
                    pygame.mixer.music.pause()
                else:
                    functionRight.play_music()
                return
            favorite_btn.config(image=favorite_btn_image)
            return
        album_music["favorite"].second.playlist.append(current_song)
        favorite_btn.config(image=favoriteBlack_btn_image)

    # Cập nhập nút favorite
    def makeBtn_favorite():
        if album_music["favorite"].second.playlist.search(current_song) != None:
            favorite_btn.config(image=favoriteBlack_btn_image)
        else:
            favorite_btn.config(image=favorite_btn_image)

    # Cập nhập lable album
    def album_music(type):
        global album
        album = type
        functionRight.check_album()
    # check để tạo Album
    def check_album():
        global index 
        index = 0
        functionRight.make_list(album_music[album].second)

    # Hiển thị danh sách nhạc trong album
    def make_list(type):
        global current_song, index, album
        label_album.configure(image="", text=album.title(), font=myFont)
        songlist1.delete(0, END)
        song2list.playlist.clear()
        song2list.clear_playlist()
        current = type.playlist.head
        while current is not None:
            song2list.playlist.append(current.data)
            songlist1.insert("end", current.data)
            current = current.next
        song2list.current_song_node = song2list.playlist.head
        # songlist1.selection_set(index)
        current_song = songlist1.get(index)
        index = 0
        functionRight.makeBtn_favorite()
        list_Trending.pack_forget()
        list_History.pack_forget()
        label_album.pack_forget()
        songlist1.pack(side=BOTTOM)
        label_album.pack(side=LEFT, pady=3)

    # Nút tìm kiếm
    def search_music():
        global album, music, index
        if search.get() == "    Search songs, album":
            return
        music = search.get()
        index = check_song_main(music, album_music["home"].second)
        print(index)
        if check_search_album(album_music, music):
            album = music.lower()
        else:
            album = "home"
            functionRight.make_list(album_music["home"].second)
            return
        functionRight.check_album()
    # Nút loa
    def volume_music():
        global volume_check
        if volume_check == False:
            slider_volume.place(x=610, y=420)
            volume_check = True
        else:
            slider_volume.place_forget()
            volume_check = False

    # Nút tạm dừng
    def pause_music():
        global temp_Pause, is_running
        if temp_Pause == False:
            pygame.mixer.music.pause()
            temp_Pause = True
            is_running = True

    # Nút phát nhạc
    def start_music():
        global temp_play, check_start
        if songlist1.size() == 0: 
            return
        if temp_play == False:
            play_btn.config(image=pause_btn_image)
            temp_play = True
            check_start = True
            functionRight.play_music()
        else:
            temp_play = False
            play_btn.config(image=play_btn_image)
            functionRight.pause_music()
    
    # Chạy nhạc 
    def play_music():
        global temp_Pause, current_song, check_start, song_length, temp_song, is_running
        temp_song = current_song
        print(temp_Pause)
        if check_start == True:
            check_start = False
        functionRight.makeBtn_favorite()
        if temp_Pause == False:
            full_path = os.path.join(root.directory, current_song) # Add the full path again
            pygame.mixer.music.load(full_path) # Load the selected song
            pygame.mixer.music.play(start=current_time) # Play the song from the current position
            pygame.mixer.music.play()
            audio = MP3(full_path)
            song_length = audio.info.length
            functionRight.play_time()
        else:
            pygame.mixer.music.unpause()
            temp_Pause = False
            is_running = False
            status_bar.after(1000, functionRight.play_time)
            
    # Chuyển bài Next, Back  
    def next_music():
        global my_slider, current_song
        if not song2list.playlist.head:
            return
        my_slider.set(0)
        if not song2list.current_song_node:
            return
        next_node = song2list.playlist.get_next(song2list.current_song_node)
        if next_node:
            song2list.current_song_node = next_node
        else:
            # Nếu không có bài hát tiếp theo, chọn bài hát đầu tiên
            song2list.current_song_node = song2list.playlist.head
        # Lấy dữ liệu từ nút hiện tại và thực hiện các hành động cần thiết
        current_song = song2list.current_song_node.data
        print(current_song)
        my_string = ''.join(map(str, songlist1.curselection()))
        songlist1.select_clear(0, END)
        vitri = int(my_string) + 1
        if vitri == songlist1.size():
            vitri = 0
        songlist1.select_set(vitri)
        on_double_click(event)
    def back_music():
        global my_slider, current_song
        if not song2list.playlist.head:
            return
        my_slider.set(0)
        if not song2list.current_song_node:
            return
        prev_node = song2list.playlist.get_prev(song2list.current_song_node)
        if prev_node:
            song2list.current_song_node = prev_node
        else:
            song2list.current_song_node = song2list.playlist.tail
        # Lấy dữ liệu từ nút hiện tại và thực hiện các hành động cần thiết
        current_song = song2list.current_song_node.data
        print(current_song)
        my_string = ''.join(map(str, songlist1.curselection()))
        songlist1.select_clear(0, END)
        vitri = int(my_string) - 1
        if(vitri < 0):
            vitri = songlist1.size() - 1
        songlist1.select_set(vitri)
        on_double_click(event)

    # Nút phát lại bài hát
    def restart_music():
        global temp_Restart
        if songlist1.size() == 0:
            return
        if temp_Restart == False:
            temp_Restart = True
        else:
            temp_Restart = False

    # Thanh tua nhạc
    def play_time():
        global current_song, current_time, temp_Pause, is_running
        current_time = pygame.mixer.music.get_pos() / 1000
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        current_time += 1
        if int(my_slider.get()) == int(song_length):
            my_slider.set(0)
            if temp_Restart == False:
                functionRight.next_music()
            else:
                on_double_click(event)
        elif int(my_slider.get()) == int(current_time):
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=int(current_time))
        else:
            #
            slider_position = int(song_length)
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
            my_slider.config(to=slider_position, value=int(my_slider.get()))
            status_bar.config(text=temp_song + " /" + f' {converted_current_time} / {converted_song_length} ')
            next_time = int(my_slider.get()) + 1
            my_slider.config(value=next_time)
            if is_running == False:
                status_bar.after(1000, functionRight.play_time)

# Xử lí các sự kiện 
class event():
     # Bấm vào new playlist
    def click2(event):
        global album
        if songlist2.size() == 0:
            return
        if songlist2.get(songlist2.curselection()):
            album = songlist2.get(songlist2.curselection())
        else:
            return
        functionRight.check_album()

    # Xóa playlist trong songlist2
    def rightClick_songlist2(event):
        popup_songlist2.post(event.x_root, event.y_root)

    # Thanh tua nhạc
    def slide(X):
        full_path = os.path.join(root.directory, current_song)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(start=int(my_slider.get()))

    # Textbox tìm kiếm
    def on_entry_click(event):
        # Xóa phần chữ mờ khi người dùng nhấn vào textbox
        if search.get() == "    Search songs, album":
            search.delete(0, END)
            search.config(fg="black")
    def on_focusout(event):
        # Hiện lại phần chữ mờ khi người dùng rời khỏi search
        if search.get() == "":   
            search.insert(0, "    Search songs, album")
            search.config(fg="grey")

# Nút bấm frameleft
home_btn_image = PhotoImage(file='./images/home.png')
trend_btn_image = PhotoImage(file='./images/trending.png')
add_btn_image = PhotoImage(file ='./images/add.png')
icon_ytMusic = PhotoImage(file ='./images/icon.png')
home_btn = Button(frameLeft, text="HOME", image=home_btn_image, borderwidth=0, compound=LEFT, font=myFont, bg=temp_Color, activebackground=temp_Color, command=functionLeft.home)
trend_btn = Button(frameLeft, text="TRENDING", image=trend_btn_image, borderwidth=0, compound=LEFT, font=myFont, bg=temp_Color, activebackground=temp_Color, command=functionLeft.trending)
add_btn = Button(frameLeft, text="New playlist", image = add_btn_image, borderwidth = 0, command=functionLeft.add, compound=LEFT, font=myFont, bg=temp_Color, activebackground=temp_Color)
icon_ytMusic_lable = Label(frameLeft, text="Music", image=icon_ytMusic, borderwidth=0, compound=LEFT, font=myFont, bg=temp_Color)
icon_ytMusic_lable.grid(row=0, column=0, padx=0, pady=(0,8))
home_btn.grid(row=2, column=0, padx=7, pady=(0,4))
trend_btn.grid(row=3, column=0, padx=7, pady=4)
add_btn.grid(row=4, column=0, padx=7, pady=4)
# button frame right
# button frame 0
# tao thanh tim kiem
search_image_btn = PhotoImage(file ='./images/search.png')
search_btn = Button(frameRight0, image = search_image_btn, borderwidth=0, command=functionRight.search_music, bg=temp_Color, activebackground=temp_Color)
search_btn.grid(row=0, column=0, padx=1, pady=10)
search = Entry (frameRight0, width = 50)

# Đặt phần chữ mờ mặc định cho search
search.insert(0, "    Search songs, album")
search.config(fg="grey")
search.grid(row=0, column=1, padx=1, pady=10)
# Gán các hàm xử lý sự kiện cho search
search.bind("<FocusIn>", event.on_entry_click)
search.bind("<FocusOut>", event.on_focusout)

menu_btn_image = PhotoImage(file='./images/menu.png')
person_image = PhotoImage(file ='./images/person.png')
menu_btn = Button(frameRight0, image=menu_btn_image, borderwidth=0, bg=temp_Color, activebackground=temp_Color)
person_lable = Label(frameRight0, image=person_image, borderwidth=0, bg=temp_Color)
menu_btn.grid(row=0, column=2, padx=(210,0), pady=10, ipadx=0)
person_lable.grid(row=0, column=3, padx=(10,0), pady=10, ipadx=0)
# button frame 3
like_btn_image = PhotoImage(file='./images/like.png')
like_btn = Button(frameRight1, text="LIKED MUSIC", image=like_btn_image, borderwidth=0, compound=TOP, font=myFont, bg=temp_Color, activebackground=temp_Color, command=lambda:functionRight.album_music("favorite"))
like_btn.grid(row=0, column=0, padx=7, pady=10)
pop_btn_image = PhotoImage(file='./images/pop.png')
pop_btn = Button(frameRight1, text="POP", image=pop_btn_image, borderwidth=0, compound=TOP, font=myFont, bg=temp_Color, activebackground=temp_Color, command=lambda:functionRight.album_music("pop"))
pop_btn.grid(row=0, column=1, padx=7, pady=10)
chill_btn_image = PhotoImage(file='./images/chill.png')
chill_btn = Button(frameRight1, text="CHILL", image=chill_btn_image, borderwidth=0, compound=TOP, font=myFont, bg=temp_Color, activebackground=temp_Color, command=lambda:functionRight.album_music("chill"))
chill_btn.grid(row=0, column=2, padx=7, pady=10)
usuk_image = PhotoImage(file='./images/usuk.png')
usuk = Button(frameRight1, text="US-UK", image=usuk_image, borderwidth=0, compound=TOP, font=myFont, bg=temp_Color, activebackground=temp_Color, command=lambda:functionRight.album_music("us_uk"))
usuk.grid(row=0, column=3, padx=7, pady=10)
kpop_btn_image = PhotoImage(file='./images/kpop.png')
kpop_btn = Button(frameRight1, text="KPOP", image=kpop_btn_image, borderwidth=0, compound=TOP, font=myFont, bg=temp_Color, activebackground=temp_Color, command=lambda:functionRight.album_music("kpop"))
kpop_btn.grid(row=0, column=4, padx=7, pady=10)
# button frame 5
play_btn_image = PhotoImage(file ='./images/play.png')
pause_btn_image = PhotoImage(file ='./images/pause.png')
next_btn_image = PhotoImage(file ='./images/skip_next.png')
back_btn_image = PhotoImage(file ='./images/skip_pre.png')
restart_btn_image = PhotoImage(file ='./images/restart.png')
favorite_btn_image = PhotoImage(file ='./images/favorite.png')
favoriteBlack_btn_image = PhotoImage(file ='./images/favorite_black.png')
volume_btn_image = PhotoImage(file ='./images/volume.png')

play_btn = Button(frameRight3, image = play_btn_image, borderwidth = 0, bg=temp_Color, activebackground=temp_Color, command = functionRight.start_music)
next_btn = Button(frameRight3, image = next_btn_image, borderwidth = 0, bg=temp_Color, activebackground=temp_Color, command = functionRight.next_music)
back_btn = Button(frameRight3, image = back_btn_image, borderwidth = 0, bg=temp_Color, activebackground=temp_Color, command = functionRight.back_music)
restart_btn = Button(frameRight3, image = restart_btn_image, borderwidth=0, bg=temp_Color, activebackground=temp_Color, command=functionRight.restart_music)
favorite_btn = Button(frameRight3, image = favorite_btn_image, borderwidth=0, bg=temp_Color, activebackground=temp_Color, command=functionRight.favorite_music)
volume_btn = Button(frameRight3, image = volume_btn_image, borderwidth=0, bg=temp_Color, activebackground=temp_Color, command=functionRight.volume_music)

# vi tri cac nut
play_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
back_btn.grid(row=0, column=1, padx=7, pady=10)
restart_btn.grid(row=0, column=4, padx=7, pady=10)
favorite_btn.grid(row=0, column=5, padx=7, pady=10)
volume_btn.grid(row=0, column=6, padx=7, pady=10)

# Hiển thị tên Album đang mở
label_album = Label(frameRight2, bg=temp_Color)

# Hiển thị danh sách nhạc của Album đang mở
songlist1 = Listbox(frameRight2, bg=temp_Color, fg="black", width=100, height=10, borderwidth=5)
list_Trending = Listbox(frameRight2, bg=temp_Color, fg="black", width=100, height=10, borderwidth=5)
list_History = Listbox(frameRight2, bg=temp_Color, fg="black", width=100, height=10, borderwidth=5)

# Tạo menu chuột phải
popup_menu0 = Menu(songlist1, tearoff=0)
remove_btn_image = PhotoImage(file ='./images/delete.png')
playlist_add_btn_image = PhotoImage(file ='./images/playlist_add.png')
favorite_btn_image = PhotoImage(file ='./images/favorite.png')
popup_menu0.add_command(label="Add to liked songs", image=favorite_btn_image, compound=LEFT, command=functionRight.favorite_music)
popup_menu0.add_command(label="Save to playlist", image=playlist_add_btn_image, compound=LEFT, command=save_playlist)
popup_menu0.add_command(label="Remove from queue", image=remove_btn_image, compound=LEFT, command=functionRight.delete_music)

popup_menu1 = Menu(menu_btn, tearoff=0)
history_btn_image = PhotoImage(file ='./images/history.png')
popup_menu1.add_command(label="History", image=history_btn_image, compound=LEFT, command=functionRight.History)
color_btn_image = PhotoImage(file ='./images/dark_mode.png')
popup_menu1.add_command(label="Color", image=color_btn_image, compound=LEFT, command=functionRight.Color)

popup_history = Menu(list_History, tearoff=0)
popup_history.add_command(label="Remove from history", image=remove_btn_image, compound=LEFT, command=delete_history)

# tao listMain
functionLeft.home()

# xu ly su kien
songlist2.bind("<Button-1>", event.click2)
popup_songlist2 = Menu(songlist2, tearoff=0)
popup_songlist2.add_command(label="Delete playlist", image=remove_btn_image, compound=LEFT, command=functionLeft.delete_new_playlist)

songlist2.bind("<Button-3>", event.rightClick_songlist2)


songlist1.bind("<Button-3>", functionRight.right_click)
songlist1.bind("<Double-Button-1>", on_double_click)
songlist1.bind("<<ListboxSelect>>", on_select)
menu_btn.bind("<Button-1>", functionRight.left_click)
list_History.bind("<Button-3>", functionRight.right_click_history)
selected_index = None

songlist1.bind("<Button-1>", on_listbox_click)
songlist1.bind("<B1-Motion>", on_listbox_motion)
# Tạo một Text widget để hiển thị lịch sử
history_listbox = Listbox()
# Tạo Listbox để hiển thị số lần nhấn vào từng mục
trending_listbox = Listbox()
# Thiết lập style cho thanh slider
style = ttk.Style()
style.configure("TScale", background=temp_Color)
# tao slider
my_slider = ttk.Scale(frameRight4, from_= 0, to=100, orient=HORIZONTAL, value=0, command=event.slide, length=360, style="TScale")
my_slider.pack(pady=3)

# thanh tang giam am luong
slider_volume = Scale(root, length=70, width=10, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg=temp_Color)
slider_volume.set(50) # Set the initial valu

# thanh bar
status_bar = Label(frameRight4, text='', bd=1, anchor=E, bg= temp_Color)
status_bar.pack(fill=X, side=BOTTOM, ipady=0)

search_btn.invoke()
root.bind('<Return>', lambda event: search_btn.invoke())
# Cập nhật cửa sổ
root.update_idletasks()
root.mainloop()