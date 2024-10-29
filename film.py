import pandas as pd
import ast
from mlxtend.frequent_patterns import fpgrowth, association_rules

def NormalizeMovies(writeFile):
    movies = pd.read_csv("film_veri/movie.csv")

    Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
    movies_filtered = movies[movies["genres"].str.contains('|'.join(Kategoriler))]

    if(writeFile):
        movies_filtered.to_csv("film_veri_normalized/movies_normalized.csv", index=False)

def NormalizeViews(writeFile):
    rating = pd.read_csv("film_veri/rating.csv", usecols=["userId", "movieId"])

    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv", usecols=["movieId"])

    movieList = movies["movieId"].tolist()

    rating_filtered = rating[rating["movieId"].isin(list(movieList))]

    if(writeFile):
        rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False)


def NormalizeUsers(writeFile):
    rating = pd.read_csv("film_veri_normalized/views_normalized.csv")

    userWithMovies = rating.groupby(["userId"], as_index=False).agg({"movieId" : list})

    if(writeFile):
        userWithMovies.to_csv("film_veri_normalized/user_normalized.csv", index=False)


def FindPopularFilms(writeFile):
    Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
    views = pd.read_csv("film_veri_normalized/views_normalized.csv")
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")

    popularMoviesDF = pd.DataFrame(columns=["category", "movies"])

    for kategori in Kategoriler:
        moviesNew = movies[movies['genres'].str.contains(kategori)]["movieId"].values.tolist()
        filteredViews = views[views["movieId"].isin(moviesNew)]
        popularMovies = filteredViews["movieId"].value_counts().head(50).index.tolist()
        popularMoviesDF.loc[len(popularMoviesDF)] = [kategori, popularMovies]

    if(writeFile):
        popularMoviesDF.to_csv("film_veri_normalized/popular_movies.csv", index=False)


def CreateMatris(writeFile):

    userWmovies = pd.read_csv("film_veri_normalized/user_normalized.csv")
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")
    
    movieList = movies["movieId"].tolist() 
    userList = userWmovies["userId"].tolist()

    userWmovies["movieId"] = userWmovies["movieId"].apply(ast.literal_eval)
 
    user_movie_matrix = pd.DataFrame(False, index=userList, columns=movieList)
    for _,row in userWmovies.iterrows():
        user_movie_matrix.loc[row["userId"], row["movieId"]] = True

    if(writeFile):
        user_movie_matrix.to_csv("film_veri_normalized/matris.csv", index=False)
    
    return user_movie_matrix


def CreateRules(minsupport, liftthreshold, writeFile):
    usermoviematrix = CreateMatris(False)
    frequent_itemsets = fpgrowth(usermoviematrix, min_support=minsupport, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=liftthreshold)
    if(writeFile):
        rules.to_csv("Rules/rules.csv", index=False)


def frozenset_string_to_list(frozenset_str):
    items = frozenset_str.replace('frozenset(', '').replace(')', '').strip('{}').split(', ')
    return list(map(int, items))


def SuggestFilms(movieId):
    rules = pd.read_csv("Rules/rules.csv")
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")

    rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list)
    rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list)
    
    filtered_rules = rules[rules["antecedents"].apply(lambda x: x == movieId)]
    filtered_rules = filtered_rules.sort_values(by="lift", ascending=False)
    filtered_rules["consequents_len"] = filtered_rules["consequents"].apply(lambda x: len(x))

    suggestionIds = sum(filtered_rules[filtered_rules["consequents_len"] >= 1]["consequents"].head(20), [])
    suggestions = []

    for suggest in suggestionIds:
        suggestTitle = movies[movies["movieId"] == suggest]["title"].values[0]
        suggestions.append(suggestTitle)

    return suggestions



    



















