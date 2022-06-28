import math
from operator import itemgetter
import pandas as pd
import recommender_without_fav_game
import itertools

column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv',sep=',',names=column_names)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv',sep=',', names=column_names)

ratings = pd.merge(ratings, board_titles, on='item_id')
# ratings.groupby('title')['rating'].mean()
# ratings.groupby('title')['rating'].mean().sort_values(ascending=False).head()
ratings_df = pd.DataFrame(ratings.groupby('title')['rating'].mean())
ratings_df.rename(columns={'rating': 'average_rating'}, inplace=True)
ratings_df['num_of_ratings'] = pd.DataFrame(ratings.groupby('title')['rating'].count())


user_board_matrix = ratings.pivot_table(values='rating', index='title', columns='user_id')


zombiciders = []
zombiciders_count = {}
dixiters = []
dixiters_count = {}
gloomhaveners = []
gloomhaveners_count = {}
terraformers = []
terraformers_count = {}

for id in user_board_matrix.columns:
    count = 0
    for k, v in user_board_matrix[id].dropna(inplace=False).items():
        count += 1
        if k == 'Zombicide':
            if v == 10:
                zombiciders.append(id)
        if k == 'Dixit':
            if v == 10:
                dixiters.append(id)
        if k == 'Gloomhaven':
            if v == 10:
                gloomhaveners.append(id)
        if k == 'Terraforming Mars':
            if v == 10:
                terraformers.append(id)


print('Zombiciders: ', len(zombiciders))
print('Dixiters: ', len(dixiters))
print('Gloomhaveners', len(gloomhaveners))


for zombicider in zombiciders:
    zombiciders_count[zombicider] = len(user_board_matrix[zombicider].dropna(inplace=False))

for dixiter in dixiters:
    dixiters_count[dixiter] = len(user_board_matrix[dixiter].dropna(inplace=False))

for gloomhavener in gloomhaveners:
    gloomhaveners_count[gloomhavener] = len(user_board_matrix[gloomhavener].dropna(inplace=False))

for terraformer in terraformers:
    terraformers_count[terraformer] = len(user_board_matrix[terraformer].dropna(inplace=False))

oz = sorted(zombiciders_count.items(), key=itemgetter(1), reverse=True)
top10_z = []
for i in oz[0:12]:
    top10_z.append([i[0]])


od = sorted(dixiters_count.items(), key=itemgetter(1), reverse=True)
top10_d = []
for i in od[0:12]:
    top10_d.append([i[0]])


og = sorted(gloomhaveners_count.items(), key=itemgetter(1), reverse=True)
top10_g = []
for i in og[0:12]:
    top10_g.append([i[0]])

ot = sorted(terraformers_count.items(), key=itemgetter(1), reverse=True)
top10_t = []
for i in ot[0:12]:
    top10_t.append([i[0]])


#
# print('top 12 zombicide')
# scores_z = 0
# logi = 1
# for comb in itertools.combinations(top10_z, 4):
#     ids = []
#     for i in comb:
#         for j in i:
#             ids.append(j)
#     try:
#         score = recommender_without_fav_game.getIndex(ids, 'Zombicide')
#     except KeyError:
#         score = None
#     print(f'Score for comb: {ids} is {score}.')
#     if score <= 10:
#         score = 2
#     elif score <= 20:
#         score = 1
#     elif score <= 50:
#         score = 0
#     else:
#         score = -1
#     print(f'Score for comb after normalization: {ids} is {score}.')
#     score = score/math.log2(logi+1)
#     print(f'Score for comb with log: {ids} is {score}.')
#     scores_z += score
#     logi += 1
#
#
# print('top 12 dixit')
# scores_d = 0
# logi = 1
# for comb in itertools.combinations(top10_d, 4):
#     ids = []
#     for i in comb:
#         for j in i:
#             ids.append(j)
#     try:
#         score = recommender_without_fav_game.getIndex(ids, 'Dixit')
#     except KeyError:
#         score = None
#     print(f'Score for comb: {ids} is {score}.')
#     if score <= 10:
#         score = 2
#     elif score <= 20:
#         score = 1
#     elif score <= 50:
#         score = 0
#     else:
#         score = -1
#     print(f'Score for comb after normalization: {ids} is {score}.')
#     score = score/math.log2(logi+1)
#     print(f'Score for comb with log: {ids} is {score}.')
#     scores_d += score
#     logi += 1

#
# print('top 12 gloomhaven')
# scores_g = 0
# logi = 1
# for comb in itertools.combinations(top10_g, 4):
#     ids = []
#     for i in comb:
#         for j in i:
#             ids.append(j)
#     try:
#         score = recommender_without_fav_game.getIndex(ids, 'Gloomhaven')
#     except KeyError:
#         score = None
#     if score is None:
#         score = -1
#     else:
#         print(f'Score for comb: {ids} is {score}.')
#         if score <= 10:
#             score = 2
#         elif score <= 20:
#             score = 1
#         elif score <= 50:
#             score = 0
#         else:
#             score = -1
#     print(f'Score for comb after normalization: {ids} is {score}.')
#     score = score/math.log2(logi+1)
#     print(f'Score for comb with log: {ids} is {score}.')
#     scores_g += score
#     logi += 1

print('top 12 terraforming mars')
scores_t = 0
logi = 1
for comb in itertools.combinations(top10_t, 4):
    ids = []
    for i in comb:
        for j in i:
            ids.append(j)
    try:
        score = recommender_without_fav_game.getIndex(ids, 'Terraforming Mars')
    except KeyError:
        score = None
    if score is None:
        score = -1
    else:
        print(f'Score for comb: {ids} is {score}.')
        if score <= 10:
            score = 2
        elif score <= 20:
            score = 1
        elif score <= 50:
            score = 0
        else:
            score = -1
    print(f'Score for comb after normalization: {ids} is {score}.')
    score = score/math.log2(logi+1)
    print(f'Score for comb with log: {ids} is {score}.')
    scores_t += score
    logi += 1
#
# print(f'Score for Gloomhaveners: {scores_g}')
# print(f'Score for Zombiciders: {scores_z}')
# print(f'Score for Dixiters: {scores_d}')
print(f'Score for Terraformers: {scores_t}')
