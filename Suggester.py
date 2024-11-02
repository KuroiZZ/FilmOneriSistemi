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

    suggestionIds_unique = []
    for Id in suggestionIds:
        if(Id not in suggestionIds_unique):
            suggestionIds_unique.append(Id)

    suggests = IdtoTitleConvertor(suggestionIds_unique)

    return suggests
