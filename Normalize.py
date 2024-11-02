import pandas as pd

def NormalizeMovies(writeFile):
    movies = pd.read_csv("film_veri/movie.csv")

    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]

    movies_filtered = movies[movies["genres"].str.contains('|'.join(categories))]

    if(writeFile):
        movies_filtered.to_csv("film_veri_normalized/movies_normalized.csv", index=False)
    else:
        print(movies_filtered)

def NormalizeViews(writeFile):
    views = pd.read_csv("film_veri/rating.csv", usecols=["userId", "movieId"])

    movie_list = pd.read_csv("film_veri_normalized/movies_normalized.csv")["movieId"].tolist()

    rating_filtered = views[views["movieId"].isin(list(movie_list))]

    if(writeFile):
        rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False)
    else:
        print(rating_filtered)

def NormalizeUsers(writeFile):
    views = pd.read_csv("film_veri_normalized/views_normalized.csv")

    user_with_movies = views.groupby(["userId"], as_index=False).agg({"movieId" : list})

    if(writeFile):
        user_with_movies.to_csv("film_veri_normalized/user_normalized.csv", index=False)
    else:
        print(user_with_movies)

def FindPopularFilms(writeFile):
    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]

    views = pd.read_csv("film_veri_normalized/views_normalized.csv")
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")

    popular_moviesDF = pd.DataFrame(columns=["category", "movies"])

    for category in categories:
        filtered_movies = movies[movies['genres'].str.contains(category)]["movieId"].values.tolist()
        filtered_views = views[views["movieId"].isin(filtered_movies)]
        popular_movies = filtered_views["movieId"].value_counts().head(50).index.tolist()
        popular_moviesDF.loc[len(popular_moviesDF)] = [category, popular_movies]

    if(writeFile):
        popular_moviesDF.to_csv("film_veri_normalized/popular_movies.csv", index=False)
    else:
        print(popular_moviesDF)


NormalizeMovies(False)
NormalizeViews(False)
NormalizeUsers(False)
FindPopularFilms(False)


