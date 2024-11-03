import pandas as pd

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
    movies = movies[movies["category"] == category]
    movies = eval(str(movies["movies"].values[0]))
    movies = IdtoTitleConvertor(movies[0:20])
    return movies

def MoviePopularSuggest(movieId):
    movieId_list = [movieId]
    rules = pd.read_csv("Rules/rules.csv")

    rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list)
    rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list)
    
    filtered_rules = rules[rules["antecedents"].apply(lambda x: x == movieId_list)].copy()
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

    suggestionIds_unique = []
    for Id in suggestionIds:
        if(Id not in suggestionIds_unique):
            suggestionIds_unique.append(Id)

    suggests = IdtoTitleConvertor(suggestionIds_unique)

    return suggests

def CategoryPersonalSuggest(category, userId):
    users = pd.read_csv("film_veri_normalized/user_normalized.csv")
    user = users[users["userId"] == userId]
    users = None
    userMovies = eval(user["movieId"].values[0])

    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv")
    movies = movies[movies["genres"].str.contains(category)]
    movies = movies["movieId"].values.tolist()

    rules = pd.read_csv("Rules/rules.csv")

    rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list)
    rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list)
    
    filtered_rules = rules[rules["antecedents"].apply(lambda x: any(movie in x for movie in userMovies))].copy()
    filtered_rules = filtered_rules[filtered_rules["consequents"].apply(lambda x: set(x).issubset(set(movies)))]
    filtered_rules["consequents_len"] = filtered_rules["consequents"].apply(lambda x: len(x))
    filtered_rules = filtered_rules.sort_values(by=["lift", "consequents_len"], ascending=[False, True])

    indexes = filtered_rules.index.tolist()
    isFull = False
    i = 0
    suggestion_Ids = []
    while not isFull and i < len(filtered_rules):
        a = filtered_rules.loc[indexes[i], "consequents"]
        for Id in a:
            if(Id not in suggestion_Ids and Id not in userMovies):
                suggestion_Ids.append(Id)
    
        if(len(suggestion_Ids) >= 20):
            isFull = True
        i += 1

    suggestion_titles = IdtoTitleConvertor(suggestion_Ids)
    
    return suggestion_titles
    
def MoviePersonalSuggest(movieId, userId):
    users = pd.read_csv("film_veri_normalized/user_normalized.csv")
    user = users[users["userId"] == userId]
    users = None
    userMovies = eval(user["movieId"].values[0])

    movieId_list = [movieId]

    rules = pd.read_csv("Rules/rules.csv")

    rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list)
    rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list)
    
    filtered_rules = rules[rules["antecedents"].apply(lambda x: (any(movie in x for movie in userMovies) and movieId in x) or (movieId_list == x))].copy()
    a = filtered_rules["consequents"].apply(lambda x: len(x))
    filtered_rules.loc[:, "consequents_len"] = a
    filtered_rules = filtered_rules.sort_values(by=["consequents_len", "lift"], ascending=[True, False])
    
    indexes = filtered_rules.index.tolist()
    isFull = False
    i = 0
    suggestion_Ids = []
    while not isFull and i < len(filtered_rules):
        a = filtered_rules.loc[indexes[i], "consequents"]
        for Id in a:
            if(Id not in suggestion_Ids and Id not in userMovies):
                suggestion_Ids.append(Id)
    
        if(len(suggestion_Ids) >= 20):
            isFull = True
        i += 1

    suggestion_titles = IdtoTitleConvertor(suggestion_Ids)
    
    return suggestion_titles