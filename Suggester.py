import pandas as pd

def frozenset_string_to_list(frozenset_str):
    items = frozenset_str.replace('frozenset(', '').replace(')', '').strip('{}').split(', ')
    return list(map(int, items))


movies_df = pd.read_csv("film_veri_normalized/movies_normalized.csv") #Yeni oluşturulan filmler okunur

movies_df_popular = pd.read_csv("film_veri_normalized/popular_movies.csv") #Popüler filmler okunur.
 
rules = pd.read_csv("Rules/rules.csv") #kurallar okunur

users = pd.read_csv("film_veri_normalized/user_normalized.csv") #Kullanıcılar okunur

rules["antecedents"] = rules["antecedents"].apply(frozenset_string_to_list) #kurallardaki frozensetler liste haline getirilir
rules["consequents"] = rules["consequents"].apply(frozenset_string_to_list) #kurallardaki frozensetler liste haline getirilir


def IdtoTitleConvertor(movieId):
    global movies_df
    movies = [] #filmler için liste açılır.
    for movie in movieId:
        movie_title = movies_df[movies_df["movieId"] == movie]["title"].values[0] #gelen filmlerin sırayla id'ye göre filtrelenir ve ismi döndürülür.
        movies.append(movie_title)
    return movies
    
def CategoryPopularSuggest(category):
    global movies_df_popular
    movies = movies_df_popular[movies_df_popular["category"] == category] #Seçilen kategoriye göre filtrelenir.
    movies = eval(str(movies["movies"].values[0])) #Seçilen filmler stringden listeye çevirilir.
    movies = IdtoTitleConvertor(movies[0:20]) #Seçilen ilk 20 film isme dönüştürülür ve döndürülür.
    return movies

#Burda öneri seçerken head(20) yapmışsın çözmeye çalış
def MoviePopularSuggest(movieId):
    movieId_list = [movieId] #gelen id listeye dönüştürülür
    global rules

    filtered_rules = rules[rules["antecedents"].apply(lambda x: x == movieId_list)].copy() #kurallar gelen movieId'sine göre filtrelenir.
    filtered_rules = filtered_rules.sort_values(by="lift", ascending=False) #kurallar lift değerlerine göre sıralanır.
    filtered_rules["consequents_len"] = filtered_rules["consequents"].apply(lambda x: len(x)) #bir satırdaki önerilerin sayıları belirlenir.

    isFull = False
    suggestionIds = []
    i = 1
    while(not isFull):
        beforelength = len(suggestionIds) #giriş uzunluğu kaydedilir
        suggestionIds_new = sum(filtered_rules[filtered_rules["consequents_len"] == i]["consequents"].head(20), []) #Öneri uzunluğuna göre sırayla eklenir.
        for Id in suggestionIds_new:
            suggestionIds.append(Id) #Seçilen öneriler kaydedilir.
        if(len(suggestionIds) == 20): #Önerilerin boyutu kontrol edilir.
            isFull = True
        if(beforelength == len(suggestionIds)): #Önerilerin boyutu değişip değişmediği kontrol edilir.
            isFull = True
        i += 1

    suggestionIds_unique = []
    for Id in suggestionIds: #Seçilen önerilerin tekrarlamasına karşın sadece eşsiz olanlar seçilir.
        if(Id not in suggestionIds_unique):
            suggestionIds_unique.append(Id)

    suggests = IdtoTitleConvertor(suggestionIds_unique) #seçilen önerilerin idleri, isme çevrilir.

    return suggests

#Burda kurallardaki önerileri filtrelerken a'ya eşitlemişsin düzelt
def CategoryPersonalSuggest(category, userId):
    global users
    global movies_df
    global rules

    user = users[users["userId"] == userId].copy() #gelen kullanıcı seçilir
    userMovies = eval(user["movieId"].values[0]) #gelen kullanıcının filmleri liste haline getirilir.

    movies = movies_df[movies_df["genres"].str.contains(category)] #filmlerden seçilen kategoriye sahip olanlar filtrelenir
    movies = movies["movieId"].values.tolist() #seçilen filmler liste haline getirilir.

    filtered_rules = rules[rules["antecedents"].apply(lambda x: any(movie in x for movie in userMovies))].copy() #kurallar kullanıcı filmleri içerenlere göre filtrelenir
    filtered_rules = filtered_rules[filtered_rules["consequents"].apply(lambda x: set(x).issubset(set(movies)))] #kurallar seçilen filmlerin alt kümesine göre filtrelenir.
    filtered_rules["consequents_len"] = filtered_rules["consequents"].apply(lambda x: len(x)) #bir satırdaki önerilerin sayıları belirlenir.
    filtered_rules = filtered_rules.sort_values(by=["lift", "consequents_len"], ascending=[False, True]) #öneri uzunluğu ve lift değerine göre sıralanır.

    indexes = filtered_rules.index.tolist() #yeni oluşan kuralların indexleri liste şekline getirilir.
    isFull = False
    i = 0
    suggestion_Ids = []
    while not isFull and i < len(filtered_rules):
        a = filtered_rules.loc[indexes[i], "consequents"] #yeni oluşan kurallardaki öneriler alınır
        for Id in a: 
            if(Id not in suggestion_Ids and Id not in userMovies): #önerilen film zaten eklenmemişse ve kullanıcı tarafından izlenmemişse önerilere eklenir.
                suggestion_Ids.append(Id)
    
        if(len(suggestion_Ids) >= 20): #Önerilerin boyutu kontrol edilir.
            isFull = True
        i += 1

    suggestion_titles = IdtoTitleConvertor(suggestion_Ids) #öneriler id'den isme çevirilir.
    
    return suggestion_titles
    
#Burda kurallardaki önerileri filtrelerken a'ya eşitlemişsin düzelt
#öneri uzunluklarını a'ya eşitlemişsin düzelt    
def MoviePersonalSuggest(movieId, userId):
    global users
    global rules

    user = users[users["userId"] == userId] #gelen kullanıcı seçilir
    userMovies = eval(user["movieId"].values[0]) #gelen kullanıcının filmleri liste haline getirilir.

    movieId_list = [movieId]

    filtered_rules = rules[rules["antecedents"].apply(lambda x: (any(movie in x for movie in userMovies) and movieId in x) or (movieId_list == x))].copy() #kurallar kullanıcının filmlerini içeriyor mu ve içlerinde seçilen film var mı diye filtrelenir veya seçilen filme eşit mi diye filtrelenir.
    a = filtered_rules["consequents"].apply(lambda x: len(x)) #önerilerin uzunlukları kaydedilir
    filtered_rules.loc[:, "consequents_len"] = a #önerilerin uzunlukları dataframe'e eklenir
    filtered_rules = filtered_rules.sort_values(by=["consequents_len", "lift"], ascending=[True, False]) #kurallar öneri uzunluğu ve lift değerine göre sıralanır.
    
    indexes = filtered_rules.index.tolist()
    isFull = False
    i = 0
    suggestion_Ids = []
    while not isFull and i < len(filtered_rules):
        a = filtered_rules.loc[indexes[i], "consequents"] #yeni oluşan kurallardaki öneriler alınır
        for Id in a:
            if(Id not in suggestion_Ids and Id not in userMovies): #önerilen film zaten eklenmemişse ve kullanıcı tarafından izlenmemişse önerilere eklenir.
                suggestion_Ids.append(Id)
    
        if(len(suggestion_Ids) >= 20): #Önerilerin boyutu kontrol edilir.
            isFull = True
        i += 1

    suggestion_titles = IdtoTitleConvertor(suggestion_Ids) #öneriler id'den isme çevirilir.
    
    return suggestion_titles