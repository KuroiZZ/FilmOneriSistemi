import pandas as pd
import time

def NormalizeFilmAndRating():
    rating = pd.read_csv('film_veri/rating.csv', usecols=["userId", "movieId"])
    movies = pd.read_csv('film_veri/movie.csv')
    Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
    movies_normalized = pd.DataFrame(columns=movies.columns)
    silinecekfilmler = []

    movieCount = 0
    selectedMovieCount = 0
    for Fkategoriler in movies["genres"]:
        Sahip = False
        for kategori in Kategoriler:
            if(kategori in Fkategoriler):
                Sahip = True
                break
        if(Sahip):
            movies_normalized.loc[selectedMovieCount] = movies.iloc[movieCount]
            selectedMovieCount +=1
        if(not Sahip):
            silinecekid = int (movies.iloc[movieCount]["movieId"])
            silinecekfilmler.append(silinecekid)
        movieCount += 1

    rating_filtered = rating[~rating["movieId"].isin(silinecekfilmler)]

    #rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False)
    #movies_normalized.to_csv("film_veri_normalized/movies_normalized.csv", index=False)

def NormalizeUsers(): #2471 Saniye sürdü kısaltmaya çalış
    rating_new = pd.read_csv("film_veri_normalized/views_normalized.csv")
    users = list(rating_new["userId"].unique())
    userWithMovies = pd.DataFrame(columns=["UserId", "Films"])

    i = 0
    for user in users:
        userMovies = list(rating_new[rating_new["userId"] == user]["movieId"])
        movieString = '|'.join(str (i) for i in userMovies)
        userWithMovies.loc[i] = [user, movieString]
        i += 1

    userWithMovies.to_csv("film_veri_normalized/user_normalized.csv", index=False)
















