import tkinter as tk
import pandas as pd
import Suggester as sg

movies = pd.read_csv("film_veri_normalized/movies_normalized.csv", usecols=["movieId", "title"]) #Filmler okunur
users = pd.read_csv("film_veri_normalized/user_normalized.csv") #Kullanıcılar okunur
suggestable_movies = pd.read_csv("film_veri_normalized/suggestable_movies.csv") #Öneri yaptırabilecek filmler okunur

def clear_screen():
    global genres_listbox_exists 
    global movie_listbox_exists
    genres_listbox_exists = False 
    movie_listbox_exists = False
    for widget in Screen.winfo_children():
        widget.destroy()

def user_selected(user_listbox, buton1, buton2):
    if user_listbox.curselection(): #gelen listboxta seçili durumun olup olmadığı kontrol edilir.
        buton1.config(state=tk.NORMAL)  #buton aktif hale getirilir
        buton2.config(state=tk.NORMAL)  #buton aktif hale getirilir
    else:
        buton1.config(state=tk.DISABLED) #buton deaktif hale getirilir
        buton2.config(state=tk.DISABLED) #buton deaktif hale getirilir

def genre_selected(genre_listbox, öner_buton):
    if genre_listbox.curselection(): #gelen listboxta seçili durumun olup olmadığı kontrol edilir.
        öner_buton.config(state=tk.NORMAL)  #buton aktif hale getirilir
    else:
        öner_buton.config(state=tk.DISABLED) #buton deaktif hale getirilir

def movie_selected(movie_listbox, öner_buton):
    if movie_listbox.curselection(): #gelen listboxta seçili durumun olup olmadığı kontrol edilir.
        öner_buton.config(state=tk.NORMAL)  #buton aktif hale getirilir
    else:
        öner_buton.config(state=tk.DISABLED) #buton deaktif hale getirilir

def suggest_category(selected_user, selected_category):
    clear_screen() #Ekran temizlenir
    if(selected_user == None): #Kullanıcı seçimi kontrol edilir
        suggestions = sg.CategoryPopularSuggest(selected_category) 
    else:
        suggestions = sg.CategoryPersonalSuggest(selected_category, selected_user)
    
    buton3 = tk.Button(Screen, text=" Geri ", width=50, command=MainScreen) #geri butonu oluşturulur
    buton3.pack(side=tk.BOTTOM, pady=20) #geri butonu eklenir

    Output_screen = tk.Text(Screen) #Çıktı ekranı oluşturulur
    for suggest in suggestions: 
        Output_screen.insert(tk.END, suggest + "\n") #Çıktı ekranına öneriler eklenir
    Output_screen.pack() #çıktı ekranı eklenir

def suggest_movie(selected_user, selected_movie):
    global movies
    selected_movie_Id = movies[movies["title"] == selected_movie]["movieId"].values[0] #filmlerden seçilen filmin idsi çekilir.
    clear_screen() #ekran temizlenir
    if(selected_user == None): #Kullanıcı seçimi kontrol edilir
        suggestions = sg.MoviePopularSuggest(selected_movie_Id)

    else:
        suggestions = sg.MoviePersonalSuggest(selected_movie_Id, selected_user)

    buton3 = tk.Button(Screen, text=" Geri ", width=50, command=MainScreen) #geri butonu oluşturulur
    buton3.pack(side=tk.BOTTOM, pady=20) #geri butonu eklenir

    Output_screen = tk.Text(Screen) #Çıktı ekranı oluşturulur
    for suggest in suggestions:
        Output_screen.insert(tk.END, suggest + "\n") #Çıktı ekranına öneriler eklenir
    Output_screen.pack() #çıktı ekranı eklenir

def MainScreen():
    clear_screen() #ekran temizlenir

    buton_frame = tk.Frame(Screen) #butonlar için bir frame oluşturulur
    buton_frame.pack(pady=80, padx=10) #frame ekrane yerleştirilir

    populer_buton = tk.Button(buton_frame, text="Popüler Film Önerileri", command=PopularScreen) #popüler film önerileri butonu oluşturulur
    kişisel_buton = tk.Button(buton_frame, text="Kişileştirilmiş Film Önerileri", command=PersonalizedScreen) #kişileştirilmiş film önerileri butonu il

    populer_buton.pack(side=tk.LEFT, padx=50) #popüler butonu ekrana eklenir
    kişisel_buton.pack(side=tk.RIGHT, padx=50) #kişileştirilmiş butonu ekrana eklenir

def PopularScreen():
    clear_screen() #ekran temizlenir
    item_frame = tk.Frame(Screen) #listbox ve diğer ürünler için bir frame oluşturuldu
    buton_frame = tk.Frame(item_frame) #butonlar için bir frame oluşturuldu.
    
    film_türü_butonu = tk.Button(buton_frame, text="Film Türüne Göre Öneriler", width=20) #film türü butonu oluşturuldu
    film_ismi_butonu = tk.Button(buton_frame, text="Film İsmine Göre Öneriler", width=20) #film ismi butonu oluşturuldu

    film_türü_butonu.pack(side=tk.LEFT, padx=50, pady=10) #film türü butonu ekrana eklendi
    film_ismi_butonu.pack(side=tk.RIGHT, padx=50, pady=10) #film ismi butonu ekrana eklendi

    film_türü_butonu.config(command=lambda: CreateGenresListbox(item_frame, None)) #film türü butonuna fonksiyon eklendi
    film_ismi_butonu.config(command=lambda: CreateMovieListbox(item_frame, None)) #film ismi butonuma fonksiyon eklendi
    buton_frame.pack(pady=(0,40)) #buton frame ekrana eklendi.

    geri_buton = tk.Button(item_frame, text=" Geri ", width=50, command=MainScreen) #geri butonu oluşturuldu
    geri_buton.pack(side=tk.BOTTOM, pady=(0,20)) #geri butonu ekrana eklendi

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True) #item frame ekrana eklendi.

def PersonalizedScreen():
    clear_screen() #ekran temizlenir 
    item_frame = tk.Frame(Screen) #listbox ve diğer ürünler için item frame oluşturulur

    user_listbox, user_listbox_frame = CreateUserListbox(item_frame) # kullanıcı listboxu ve frame'i oluşturulur

    user_listbox_frame.pack(side=tk.LEFT, fill=tk.Y) #kullanıcı frame'i ekrana eklenir
     
    buton_frame = tk.Frame(item_frame) #buton frame'i oluşturulur
    
    film_türü_butonu = tk.Button(buton_frame, text="Film Türüne Göre Öneriler", width=50, state=tk.DISABLED) #film türü butonu oluşturuldu
    film_ismi_butonu = tk.Button(buton_frame, text="Film İsmine Göre Öneriler", width=50, state=tk.DISABLED) #film ismi butonu oluşturuldu

    film_türü_butonu.pack(pady=20) #film türü butonu eklendi
    film_ismi_butonu.pack(pady=(0,20)) #film ismi butonu eklendi

    film_türü_butonu.config(command=lambda: CreateGenresListbox(buton_frame, user_listbox.get(user_listbox.curselection()))) #film türü butonuna fonksiyon eklendi
    film_ismi_butonu.config(command=lambda: CreateMovieListbox(buton_frame, user_listbox.get(user_listbox.curselection()))) #film ismi butonuna fonksiyon eklendi
    
    buton_frame.pack() #buton frame'i ekrana eklendi

    geri_butonu = tk.Button(buton_frame, text=" Geri ", width=50, command=MainScreen) #geri butonu oluşturuldu
    geri_butonu.pack(side=tk.BOTTOM) #geri butonu eklendi

    item_frame.pack(pady=10, padx=20,fill=tk.BOTH, expand=True) #item frame eklendi

    user_listbox.bind('<<ListboxSelect>>', lambda event: user_selected(user_listbox, film_türü_butonu, film_ismi_butonu)) #kullanıcı listboxuna seçildiğinde çalışan bir fonksiyon eklendi

def CreateUserListbox(item_frame):
    global users
    user_Ids = users["userId"].values.tolist() #kullanıcı idleri listeye çevirilir

    user_listbox_frame = tk.Frame(item_frame) #kullanıcı listboxu için frame oluşturulur
    
    user_listbox = tk.Listbox(user_listbox_frame) #kullanıcı listboxu oluşturulur
    user_listbox_label = tk.Label(user_listbox_frame, text = " KULLANICILAR ") #kullanıcı listboxu için label oluşturulur
    scrollbar = tk.Scrollbar(user_listbox_frame) #kullanıcı listboxu için scrollbar oluşturulur
    
    user_listbox_label.pack() #kullanıcı listboxu için label ekrana eklenir

    user_listbox.config(yscrollcommand=scrollbar.set) #kullanıcı listboxu ile scrollbar birbirine bağlanır
    user_listbox.pack(side=tk.LEFT, fill=tk.Y) #kullanıcı listboxu ekrana eklenir

    scrollbar.config(command=user_listbox.yview) #scrollbar listboxa bağlanır
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #scrollbar ekrana eklenir

    for user in user_Ids: #kullanıcı listboxuna kullanıcı idleri eklenir
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

    if not genres_listbox_exists: #tür listboxunun var olup olmadığı kontrol edilir
        if movie_listbox_exists == True: #film listboxunun var olup olmadığı kontrol edilir
            movie_listbox_frame.destroy() #movie listboxunun frame'i yok edilir
            movie_listbox_exists =False #movie listboxunun var olduğunu söyleyen değişken false yapılır
            öner_buton.destroy() #öneri butonu yok edilir

        genre_listbox_frame = tk.Frame(item_frame) #tür listboxu için frame oluşturulur
        
        genre_listbox = tk.Listbox(genre_listbox_frame, width=50) #tür listboxu oluşturulur
        genre_listbox_label = tk.Label(genre_listbox_frame, text = " TÜRLER ") #tür listboxu için label oluşturulur
        scrollbar = tk.Scrollbar(genre_listbox_frame) #tür listboxu için scrollbar oluşturulur
        
        genre_listbox_label.pack() #tür listboxu için oluşturulan label ekrana eklenir

        genre_listbox.config(yscrollcommand=scrollbar.set) #tür listboxu scrollbar ile bağlanır 
        genre_listbox.pack(side=tk.LEFT, expand=True) #tür listboxu ekrana eklenir

        scrollbar.config(command=genre_listbox.yview) #scrollbar tür listboxuna bağlanır
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #scrollbar ekrana eklenir

        genre_listbox_frame.pack(pady=(0,20)) #tür listboxu için oluşturulan frame ekrana eklenir

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50, state=tk.DISABLED) #öneri butonu oluşturulur
        öner_buton.pack(pady=(0,20)) #öneri butonu ekrana eklenir

        öner_buton.config(command= lambda:suggest_category(selected_user, genre_listbox.get(genre_listbox.curselection()))) #öneri butonuna fonksiyon eklenir

        genre_listbox.bind('<<ListboxSelect>>', lambda event: genre_selected(genre_listbox, öner_buton)) #tür listboxuna seçildiğinde çalışan bir fonksiyon eklenir

        for category in categories: #tür listboxuna türler eklenir
            genre_listbox.insert(tk.END, category)

        genres_listbox_exists = True #tür listboxunun varlığını kontrol eden değişken true yapılır

movie_listbox_exists = False
def CreateMovieListbox(item_frame, selected_user):
    global movie_listbox_exists
    global movie_listbox_frame
    global genres_listbox_exists 
    global genre_listbox_frame
    global öner_buton
    global suggestable_movies

    movie_title_list = suggestable_movies["title"].values.tolist() #film isimleri listeye dönüştürüldü

    if not movie_listbox_exists: #film listboxunun var olup olmadığı kontrol edilir
        if genres_listbox_exists == True: #tür listboxunun var olup olmadığı kontrol edilir
            genre_listbox_frame.destroy() #tür listboxunun frame'i yok edilir
            genres_listbox_exists = False #tür listboxunun varlığı false yapıldı
            öner_buton.destroy() #öneri butonu yok edilir.

        movie_listbox_frame = tk.Frame(item_frame) #film listboxunun frame'i oluşturulur
        
        movie_listbox = tk.Listbox(movie_listbox_frame, width=50) #film listboxu oluşturulur
        movie_listbox_label = tk.Label(movie_listbox_frame, text = " FİLMLER ") #film listboxu için label oluşturulur
        scrollbar = tk.Scrollbar(movie_listbox_frame) #film listboxu için scrollbar oluşturulur
        
        movie_listbox_label.pack() #film listboxu için label ekrana eklenir

        movie_listbox.config(yscrollcommand=scrollbar.set) #film listboxu scrollbara bağlandı
        movie_listbox.pack(side=tk.LEFT, expand=True) #film listboxu ekrana eklenir

        scrollbar.config(command=movie_listbox.yview) #scrollbar film listboxuna bağlanır
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #scrollbar ekrana eklenir

        movie_listbox_frame.pack(pady=(0,20)) #film listboxu ekrana eklenir

        öner_buton = tk.Button(item_frame, text=" Öner ", width=50, state=tk.DISABLED) #öneri butonu oluşturulur
        öner_buton.pack(pady=(0,20)) #öneri butonu ekrana eklenir

        öner_buton.config(command= lambda:suggest_movie(selected_user, movie_listbox.get(movie_listbox.curselection()))) #öneri butonuna fonksiyon eklenir

        movie_listbox.bind('<<ListboxSelect>>', lambda event: movie_selected(movie_listbox, öner_buton)) #film listboxunda seçilme durumunda çalışan bir fonksiyon eklendi

        for title in movie_title_list: #film listesindeki filmler listbox'a eklenir
            movie_listbox.insert(tk.END, title)

        movie_listbox_exists = True

Screen = tk.Tk()
Screen.geometry("600x410")

MainScreen()

Screen.mainloop()
