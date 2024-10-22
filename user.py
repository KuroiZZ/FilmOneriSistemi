import pandas as pd  #https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html#min-tut-02-read-write


class User:
    def __init__(self, userId, watchedMovies):
        self.userId = userId
        self.watchedMovies = watchedMovies


rating = pd.read_csv('film_veri/rating.csv', usecols=["userId", "movieId"])
Users = rating["userId"].unique()

for users in Users:
    userMovies = list(rating[rating["userId"] == users]["movieId"])
    user1 = User(1, userMovies)
    print(user1.watchedMovies)
    break








