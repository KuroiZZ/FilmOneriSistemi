import pandas as pd

movies = pd.read_csv('film_veri/movie.csv')
Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]

i = 0
for Fkategoriler in movies["genres"]:
    Sahip = False
    for kategori in Kategoriler:
        if(kategori in Fkategoriler):
            Sahip = True
            break
    if(not Sahip):
        movies = movies.drop(i)
    i += 1

movies.to_csv("film_veri_normalized/movies_normalized.csv", index=False)






