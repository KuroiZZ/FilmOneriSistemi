import pandas as pd
import ast
from mlxtend.frequent_patterns import fpgrowth, association_rules
import tkinter as tk

def NormalizeMovies(writeFile):
    movies = pd.read_csv("film_veri/movie.csv")

    categories = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]

    movies_filtered = movies[movies["genres"].str.contains('|'.join(categories))]

    if(writeFile):
        movies_filtered.to_csv("film_veri_normalized/movies_normalized.csv", index=False)

def NormalizeViews(writeFile):
    views = pd.read_csv("film_veri/rating.csv", usecols=["userId", "movieId"])

    movie_list = pd.read_csv("film_veri_normalized/movies_normalized.csv")["movieId"].tolist()

    rating_filtered = views[views["movieId"].isin(list(movie_list))]

    if(writeFile):
        rating_filtered.to_csv("film_veri_normalized/views_normalized.csv", index=False)

def NormalizeUsers(writeFile):
    views = pd.read_csv("film_veri_normalized/views_normalized.csv")

    user_with_movies = views.groupby(["userId"], as_index=False).agg({"movieId" : list})

    if(writeFile):
        user_with_movies.to_csv("film_veri_normalized/user_normalized.csv", index=False)

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

def CreateMatris(writeFile):
    user_with_movies = pd.read_csv("film_veri_normalized/user_normalized.csv")
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")
    
    movie_list = movies["movieId"].tolist() 
    user_list = user_with_movies["userId"].tolist()

    user_with_movies["movieId"] = user_with_movies["movieId"].apply(ast.literal_eval)
 
    user_movie_matrix = pd.DataFrame(False, index=user_list, columns=movie_list)
    for _,row in user_with_movies.iterrows():
        user_movie_matrix.loc[row["userId"], row["movieId"]] = True

    if(writeFile):
        user_movie_matrix.to_csv("film_veri_normalized/matris.csv", index=False)
    
    return user_movie_matrix

def CreateRules(minsupport, liftthreshold, writeFile):
    user_movie_matrix = CreateMatris(False)
    frequent_itemsets = fpgrowth(user_movie_matrix, min_support=minsupport, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=liftthreshold)
    if(writeFile):
        rules.to_csv("Rules/rules.csv", index=False)

def frozenset_string_to_list(frozenset_str):
    items = frozenset_str.replace('frozenset(', '').replace(')', '').strip('{}').split(', ')
    return list(map(int, items))

def IdtoTitleConvertor(movieId):
    moviesdf = pd.read_csv("film_veri_normalized/movies_normalized.csv")
    movies = []
    for movie in movieId:
        movie_title = moviesdf[moviesdf["movieId"] == movie]["title"].values[0]
        movies.append(movie_title)
    return movies
    
def CategoryPopularSuggest(category):
    movies = pd.read_csv("film_veri_normalized/popular_movies.csv")
    movies["movies"] = movies["movies"].apply(ast.literal_eval)
    movies = movies[movies["category"] == category]["movies"].values[0]
    movies = IdtoTitleConvertor(movies)
    return movies

def MoviePopularSuggest(movieId):
    rules = pd.read_csv("Rules/rules.csv")

    rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list)
    rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list)
    
    filtered_rules = rules[rules["antecedents"].apply(lambda x: x == movieId)]
    filtered_rules = filtered_rules.sort_values(by="lift", ascending=False)
    filtered_rules["consequents_len"] = filtered_rules["consequents"].apply(lambda x: len(x))

    isFull = False
    suggestionIds = []
    i = 1
    while(not isFull):
        beforelength = len(suggestionIds)
        suggestionIds_new = sum(filtered_rules[filtered_rules["consequents_len"] == i]["consequents"].head(20), [])
        for Id in suggestionIds_new:
            suggestionIds.append(Id)
        if(len(suggestionIds) == 20):
            isFull = True
        if(beforelength == len(suggestionIds)):
            isFull = True
        i += 1

    suggestionIds = list(set(suggestionIds))

    suggests = IdtoTitleConvertor(suggestionIds)

    return suggests

def ScreenSetup():
    Screen = tk.Tk()

    listbox_frame = tk.Frame(Screen)
    listbox_frame.pack(pady=10)

    user = pd.read_csv("film_veri_normalized/user_normalized.csv")
    user_Id = user["userId"].values.tolist()

    user_listbox = tk.Listbox(listbox_frame, height=15, width=10, activestyle="dotbox", font="Helvetica")
    user_listbox_label = tk.Label(listbox_frame, text = " USERS ")
    scrollbar = tk.Scrollbar(listbox_frame)
    
    i=1
    for user in user_Id:
        user_listbox.insert(i, user)
        i +=1

    user_listbox_label.pack()
    user_listbox.pack(side=tk.LEFT)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    user_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=user_listbox.yview)


    Screen.mainloop()
























