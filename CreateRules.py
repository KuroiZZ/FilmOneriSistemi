import pandas as pd
import ast
from mlxtend.frequent_patterns import fpgrowth, association_rules

def CreateMatris(writeFile):
    user_with_movies = pd.read_csv("film_veri_normalized/user_normalized.csv") #Yeni oluşturulan kullanıcı dosyası okunur.
    movies = pd.read_csv("film_veri_normalized/movies_normalized.csv") #Yeni oluşturulan film dosyası okunur.
    
    movie_list = movies["movieId"].tolist() #filmler liste haline getirilir
    user_list = user_with_movies["userId"].tolist() #kullanıcılar liste haline getirilir

    user_with_movies["movieId"] = user_with_movies["movieId"].apply(ast.literal_eval) #kullanıcı dataframe'indeki filmler stringden listeye çevirilir
 
    user_movie_matrix = pd.DataFrame(False, index=user_list, columns=movie_list) #matris oluşturulur
    for _,row in user_with_movies.iterrows(): #kullanıcıları tek tek alır
        user_movie_matrix.loc[row["userId"], row["movieId"]] = True #izledikleri filmleri True yapar

    if(writeFile):
        user_movie_matrix.to_csv("film_veri_normalized/matris.csv", index=False) #Matris dosyaya kaydedilir
    else:
        print(user_movie_matrix) #Matris terminalde gösterilir.
    
    return user_movie_matrix

def CreateRules(minsupport, liftthreshold, writeFile):
    user_movie_matrix = CreateMatris(False) #Matris oluşturulur.
    frequent_itemsets = fpgrowth(user_movie_matrix, min_support=minsupport, use_colnames=True) #Matris kullanılarak sık öğe kümeleri oluşturulur
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=liftthreshold) #Sık öğe kümeleri ile kurallar oluşturulur.
    if(writeFile):
        rules.to_csv("Rules/rules.csv", index=False) #Kurallar dosyaya kaydedilir
    else:
        print(rules) #Kurallar terminalde gösterilir


































