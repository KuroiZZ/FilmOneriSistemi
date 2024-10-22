import pandas as pd

movies = pd.read_csv('film_veri/movie.csv')
Kategoriler = ["Children", "Animation", "Fantasy", "War", "Horror", "Thriller", "Mystery", "Crime", "Sci-Fi", "Musical"]
movies_normalized = pd.DataFrame(columns=movies.columns)

movieCount = 0
selectedMovieCount = 0
for Fkategoriler in movies["genres"]:
    Sahip = False
    for kategori in Kategoriler:
        if(kategori in Fkategoriler):
            Sahip = True
            break
    if(Sahip):
        movies_normalized.loc[selectedMovieCount] = movies.iloc[movieCount]
        selectedMovieCount +=1
    movieCount += 1

movies_normalized.to_csv("film_veri_normalized/movies_normalized.csv", index=False)






