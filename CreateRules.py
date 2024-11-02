import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

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
    else:
        print(user_movie_matrix)
    
    return user_movie_matrix

def CreateRules(minsupport, liftthreshold, writeFile):
    user_movie_matrix = CreateMatris(False)
    frequent_itemsets = fpgrowth(user_movie_matrix, min_support=minsupport, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=liftthreshold)
    if(writeFile):
        rules.to_csv("Rules/rules.csv", index=False)
    else:
        print(rules)


































