import pandas as pd

def NormalizeMovies(writeFile):
    movies = pd.read_csv("film_veri/movie.csv") #Var olan filmleri okur

    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"] #Kullanıcılıcak kategoriler belirlenir

    movies_filtered = movies[movies["genres"].str.contains('|'.join(categories))] #İçinde belirlenen kategorilerden herhangi biri varsa alınır ve yeni bir dataframe oluşturulur

    if(writeFile):
        movies_filtered.to_csv("film_veri_normalized/movies_normalized.csv", index=False) #Yeni dataframe dosyaya kaydedilir
    else:
        print(movies_filtered) #Yeni dataframe terminalde gösterilir

def NormalizeViews(writeFile):
    views = pd.read_csv("film_veri/rating.csv", usecols=["userId", "movieId"]) #rating.csv dosyası sadece kullanıcı ve filmidleri şeklinde okunur

    movie_list = pd.read_csv("film_veri_normalized/movies_normalized.csv")["movieId"].tolist() #Yeni oluşturulan filmler okunur

    rating_filtered = views[views["movieId"].isin(list(movie_list))] #Sadece yeni oluşturulan filmleri içeren izlemeler alınır ve yeni bir dataframe oluşturukur

    if(writeFile):
        rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False) #Yeni dataframe dosyaya kaydedilir
    else:
        print(rating_filtered) #Yeni dataframe terminalde gösterilir

def NormalizeUsers(writeFile):
    views = pd.read_csv("film_veri_normalized/views_normalized.csv") #Yeni oluşturulan izlemeler okunur

    user_with_movies = views.groupby(["userId"], as_index=False).agg({"movieId" : list}) #Bu izlemeler kullanılarak kullanıcı ve onun izlediği filmler satır haline getirilir

    if(writeFile):
        user_with_movies.to_csv("film_veri_normalized/user_normalized.csv", index=False) #Yeni dataframe dosyaya kaydedilir
    else:
        print(user_with_movies) #Yeni dataframe terminalde gösterilir.

def FindPopularFilms(writeFile):
    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"] #Kategoriler oluşturulur

    views = pd.read_csv("film_veri_normalized/views_normalized.csv") #İzlemeler dosyası okunur
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv") #Filmler dosyası okunur

    popular_moviesDF = pd.DataFrame(columns=["category", "movies"]) #Yeni bir dataframe oluşturulur

    for category in categories:
        filtered_movies = movies[movies['genres'].str.contains(category)]["movieId"].values.tolist() #Belirlediğimiz kategorilere ait filmler filtrelenir ve liste haline getirilir.
        filtered_views = views[views["movieId"].isin(filtered_movies)] #İzlemeler yeni belirlediğimiz filmlere göre filtrelenir
        popular_movies = filtered_views["movieId"].value_counts().head(50).index.tolist() #İzlemelerde en yüksek izlenmeye sahip 50 film listelenir
        popular_moviesDF.loc[len(popular_moviesDF)] = [category, popular_movies] #Bulunan filmler ve kategori yeni dataframe'e kaydedilir

    if(writeFile):
        popular_moviesDF.to_csv("film_veri_normalized/popular_movies.csv", index=False) #Yeni dataframe dosyaya kaydedilir
    else:
        print(popular_moviesDF) #Yeni dataframe terminalde gösterilir


NormalizeMovies(False)
NormalizeViews(False)
NormalizeUsers(False)
FindPopularFilms(False)


