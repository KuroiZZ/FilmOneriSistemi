import tkinter as tk
import pandas as pd
import Suggester as sg

def clear_screen():
    global genres_listbox_exists 
    global movie_listbox_exists
    genres_listbox_exists = False
    movie_listbox_exists = False
    for widget in Screen.winfo_children():
        widget.destroy()

def user_selected(user_listbox, buton1, buton2):
    if user_listbox.curselection():
        buton1.config(state=tk.NORMAL)  
        buton2.config(state=tk.NORMAL)  
    else:
        buton1.config(state=tk.DISABLED)  
        buton2.config(state=tk.DISABLED)

def genre_selected(genre_listbox, öner_buton):
    if genre_listbox.curselection():
        öner_buton.config(state=tk.NORMAL)  
    else:
        öner_buton.config(state=tk.DISABLED)  

def movie_selected(movie_listbox, öner_buton):
    if movie_listbox.curselection():
        öner_buton.config(state=tk.NORMAL)  
    else:
        öner_buton.config(state=tk.DISABLED)  

def suggest_category(selected_user, selected_category):
    clear_screen()
    if(selected_user == None):
        suggestions = sg.CategoryPopularSuggest(selected_category)
    else:
        suggestions = sg.CategoryPersonalSuggest(selected_category, selected_user)
    
    buton3 = tk.Button(Screen, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM, pady=20)

    Output_screen = tk.Text(Screen)
    for suggest in suggestions:
        Output_screen.insert(tk.END, suggest + "\n")
    Output_screen.pack()

def suggest_movie(selected_user, selected_movie):
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv", usecols=["movieId", "title"])
    selected_movie_Id = movies[movies["title"] == selected_movie]["movieId"].values[0]
    clear_screen()
    if(selected_user == None):
        suggestions = sg.MoviePopularSuggest(selected_movie_Id)

    else:
        suggestions = sg.MoviePersonalSuggest(selected_movie_Id, selected_user)

    buton3 = tk.Button(Screen, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM, pady=20)

    Output_screen = tk.Text(Screen)
    for suggest in suggestions:
        Output_screen.insert(tk.END, suggest + "\n")
    Output_screen.pack()

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

    buton1.config(command=lambda: CreateGenresListbox(item_frame, None))
    buton2.config(command=lambda: CreateMovieListbox(item_frame, None))

    buton_frame.pack(pady=(0,40))

    buton3 = tk.Button(item_frame, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM, pady=(0,20))

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True)

def PersonalizedScreen():
    clear_screen()
    item_frame = tk.Frame(Screen)

    user_listbox, user_listbox_frame = CreateUserListbox(item_frame)   

    user_listbox_frame.pack(side=tk.LEFT, fill=tk.Y)
     
    buton_frame = tk.Frame(item_frame)
    
    buton1 = tk.Button(buton_frame, text="Film Türüne Göre Öneriler", width=50, state=tk.DISABLED)
    buton2 = tk.Button(buton_frame, text="Film İsmine Göre Öneriler", width=50, state=tk.DISABLED)

    buton1.pack(pady=20)
    buton2.pack(pady=(0,20))

    buton1.config(command=lambda: CreateGenresListbox(buton_frame, user_listbox.get(user_listbox.curselection())))
    buton2.config(command=lambda: CreateMovieListbox(buton_frame, user_listbox.get(user_listbox.curselection())))
    
    buton_frame.pack()

    buton3 = tk.Button(buton_frame, text=" Geri ", width=50, command=MainScreen)
    buton3.pack(side=tk.BOTTOM)

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True)

    user_listbox.bind('<<ListboxSelect>>', lambda event: user_selected(user_listbox, buton1, buton2))

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

    for user in user_Ids:
        user_listbox.insert(tk.END, user)

    return user_listbox, user_listbox_frame

öner_buton = None
genres_listbox_exists = False
def CreateGenresListbox(item_frame, selected_user):
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

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50, state=tk.DISABLED)
        öner_buton.pack(pady=(0,20))

        öner_buton.config(command= lambda:suggest_category(selected_user, genre_listbox.get(genre_listbox.curselection())))

        genre_listbox.bind('<<ListboxSelect>>', lambda event: genre_selected(genre_listbox, öner_buton))

        for category in categories:
            genre_listbox.insert(tk.END, category)

        genres_listbox_exists = True

movie_listbox_exists = False
def CreateMovieListbox(item_frame, selected_user):
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

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50, state=tk.DISABLED)
        öner_buton.pack(pady=(0,20))

        öner_buton.config(command= lambda:suggest_movie(selected_user, movie_listbox.get(movie_listbox.curselection())))

        movie_listbox.bind('<<ListboxSelect>>', lambda event: movie_selected(movie_listbox, öner_buton))

        for title in movie_title_list:
            movie_listbox.insert(tk.END, title)

        movie_listbox_exists = True

Screen = tk.Tk()
Screen.geometry("600x410")

MainScreen()

Screen.mainloop()
