import pandas as pd
from recommender_without_fav_game import getIndex

column_names = ['user_id', 'item_id', 'rating']
users = pd.read_csv('userratings.csv', sep=',', names=column_names)
print(len(users['user_id'].unique()))
jogo = 'Gloomhaven'
count = 0
gamers = []
scores = []
for user in users['user_id'].unique():
    if count < 4:
        count += 1
        gamers.append(user)
    else:
        count = 0
        try:
            index = getIndex(gamers, jogo)
        except KeyError:
            index = None
        print(gamers)
        print('Index: ', index)
        gamers = []
