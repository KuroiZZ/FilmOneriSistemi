import pandas as pd

def NormalizeMovies():
    movies = pd.read_csv('film_veri/movie.csv')

    Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
    movies_filtered = movies[movies["genres"].str.contains('|'.join(Kategoriler))]

    #movies_filtered.to_csv("film_veri_normalized/movies_normalized.csv", index=False)

def NormalizeViews():
    rating = pd.read_csv("film_veri/rating.csv", usecols=["userId", "movieId"])

    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv", usecols=["movieId"])

    movieList = movies["movieId"].tolist()

    rating_filtered = rating[rating["movieId"].isin(list(movieList))]

    #rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False)


def NormalizeUsers():
    rating = pd.read_csv("film_veri_normalized/views_normalized.csv")

    userWithMovies = rating.groupby(["userId"], as_index=False).agg({'movieId' : lambda x: '|'.join(map(str, x))})

    #userWithMovies.to_csv("film_veri_normalized/user_normalized.csv", index=False)
    



















