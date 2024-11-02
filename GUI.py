import tkinter as tk
import pandas as pd

def clear_screen():
    for widget in Screen.winfo_children():
        widget.destroy()

def MainScreen():
    clear_screen()

    buton_frame = tk.Frame(Screen)
    buton_frame.pack(pady=80, padx=10)

    buton1 = tk.Button(buton_frame, text="Popüler Film Önerileri", command=PopularScreen)
    buton2 = tk.Button(buton_frame, text="Kişileştirilmiş Film Önerileri", command=PersonalizedScreen)

    buton1.pack(side=tk.LEFT, padx=50)
    buton2.pack(side=tk.RIGHT, padx=50)

def PopularScreen():
    clear_screen()
    item_frame = tk.Frame(Screen)
    buton_frame = tk.Frame(item_frame)
    
    buton1 = tk.Button(buton_frame, text="Film Türüne Göre Öneriler", width=20)
    buton2 = tk.Button(buton_frame, text="Film İsmine Göre Öneriler", width=20)

    buton1.pack(side=tk.LEFT, padx=50, pady=10)
    buton2.pack(side=tk.RIGHT, padx=50, pady=10)

    buton1.config(command=lambda: CreateGenresListbox(item_frame))
    buton2.config(command=lambda: CreateMovieListbox(item_frame))

    buton_frame.pack(pady=(0,40))

    buton3 = tk.Button(item_frame, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM, pady=(0,20))

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True)

def PersonalizedScreen():
    clear_screen()
    item_frame = tk.Frame(Screen)

    CreateUserListbox(item_frame)    

    buton_frame = tk.Frame(item_frame)
    
    buton1 = tk.Button(buton_frame, text="Film Türüne Göre Öneriler", width=50)
    buton2 = tk.Button(buton_frame, text="Film İsmine Göre Öneriler", width=50)

    buton1.pack(pady=20)
    buton2.pack(pady=(0,20))

    buton1.config(command=lambda: CreateGenresListbox(buton_frame))
    buton2.config(command=lambda: CreateMovieListbox(buton_frame))

    buton_frame.pack()

    buton3 = tk.Button(buton_frame, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM)

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True)

def CreateUserListbox(item_frame):
    user = pd.read_csv("film_veri_normalized/user_normalized.csv")
    user_Ids = user["userId"].values.tolist()

    user_listbox_frame = tk.Frame(item_frame)
    
    user_listbox = tk.Listbox(user_listbox_frame)
    user_listbox_label = tk.Label(user_listbox_frame, text = " USERS ")
    scrollbar = tk.Scrollbar(user_listbox_frame)
    
    user_listbox_label.pack()

    user_listbox.config(yscrollcommand=scrollbar.set)
    user_listbox.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar.config(command=user_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    user_listbox_frame.pack(side=tk.LEFT, fill=tk.Y)

    for user in user_Ids:
        user_listbox.insert(tk.END, user)

öner_buton = None
genres_listbox_exists = False
def CreateGenresListbox(item_frame):
    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
    global genres_listbox_exists 
    global genre_listbox_frame
    global movie_listbox_exists
    global movie_listbox_frame
    global öner_buton

    if not genres_listbox_exists:
        if movie_listbox_exists == True:
            movie_listbox_frame.destroy()
            movie_listbox_exists =False
            öner_buton.destroy()

        genre_listbox_frame = tk.Frame(item_frame)
        
        genre_listbox = tk.Listbox(genre_listbox_frame, width=50)
        genre_listbox_label = tk.Label(genre_listbox_frame, text = " GENRES ")
        scrollbar = tk.Scrollbar(genre_listbox_frame)
        
        genre_listbox_label.pack()

        genre_listbox.config(yscrollcommand=scrollbar.set)
        genre_listbox.pack(side=tk.LEFT, expand=True)

        scrollbar.config(command=genre_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        genre_listbox_frame.pack(pady=(0,20))

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50)
        öner_buton.pack(pady=(0,20))

        for category in categories:
            genre_listbox.insert(tk.END, category)

        genres_listbox_exists = True

movie_listbox_exists = False
def CreateMovieListbox(item_frame):
    global movie_listbox_exists
    global movie_listbox_frame
    global genres_listbox_exists 
    global genre_listbox_frame
    global öner_buton

    movie = pd.read_csv("film_veri_normalized/movies_normalized.csv")
    movie_title_list = movie["title"].values.tolist()

    if not movie_listbox_exists:
        if genres_listbox_exists == True:
            genre_listbox_frame.destroy()
            genres_listbox_exists = False
            öner_buton.destroy()

        movie_listbox_frame = tk.Frame(item_frame)
        
        movie_listbox = tk.Listbox(movie_listbox_frame, width=50)
        movie_listbox_label = tk.Label(movie_listbox_frame, text = " MOVIES ")
        scrollbar = tk.Scrollbar(movie_listbox_frame)
        
        movie_listbox_label.pack()

        movie_listbox.config(yscrollcommand=scrollbar.set)
        movie_listbox.pack(side=tk.LEFT, expand=True)

        scrollbar.config(command=movie_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        movie_listbox_frame.pack(pady=(0,20))

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50)
        öner_buton.pack(pady=(0,20))

        for title in movie_title_list:
            movie_listbox.insert(tk.END, title)

        movie_listbox_exists = True

Screen = tk.Tk()
Screen.geometry("600x410")

MainScreen()

Screen.mainloop()
