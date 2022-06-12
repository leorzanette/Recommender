import pandas as pd
import numpy as np
column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv', sep=',', names=column_names)
# print(ratings['user_id'].nunique())
# print('ratings')
# print(ratings)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv', sep=',', names=column_names)
# print('board_titles')
# print(board_titles)
df = pd.merge(ratings, board_titles, on='item_id', how='inner')
# print('df')
# print(df)
agg_ratings = df.groupby('title').agg(mean_rating=('rating', 'mean'),
                                      number_of_ratings=('rating', 'count')).reset_index()
# print('agg_ratings')
# print(agg_ratings)
agg_ratings_GT100 = agg_ratings[agg_ratings['number_of_ratings'] > 30]
agg_ratings_GT100.sort_values(by='number_of_ratings', ascending=False).head()
# print('agg_ratings_GT100')
# print(agg_ratings_GT100)
df_GT100 = pd.merge(df, agg_ratings_GT100[['title']], on='title', how='inner')
# print('df_GT100')
# print(df_GT100)
matrix = df_GT100.pivot_table(index='user_id', columns='title', values='rating')
# print('matrix')
# print(matrix)
matrix_norm = matrix#.subtract(matrix.mean(axis=1), axis='rows')
# print('matrix_norm')
# print(matrix_norm)

def predictionWithout(id, jogo):
    matrix_norm.at[id, jogo] = np.nan
    user_similarity = matrix_norm.T.corr()
    # print(user_similarity)
    user_similarity_threshold = 0.3
    n = 10
    similar_users = user_similarity[user_similarity[id] > user_similarity_threshold][id].sort_values(
        ascending=False)[:n]

    picked_userid_played = matrix_norm[matrix_norm.index == id].dropna(axis=1, how='all')

    similar_user_boards = matrix_norm[matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
    # similar_user_boards.drop(picked_userid_played.columns, axis=1, inplace=True, errors='ignore')
    item_score = {}
    for i in similar_user_boards.columns:
        board_rating = similar_user_boards[i]
        upper = 0
        lower = 0
        board_rating_sum = 0
        board_count = 0

        for u in similar_users.index:
            if not pd.isna(board_rating[u]):
                board_rating_sum += board_rating[u]
                board_count += 1
            if not pd.isna(board_rating[u]):
                upper += (similar_users[u] * (board_rating[u] - (board_rating_sum / board_count)))
                lower += similar_users[u]
        item_score[i] = upper / lower
    item_score = pd.DataFrame(item_score.items(), columns=['board', 'board_score'])

    ranked_item_score = item_score.sort_values(by='board_score', ascending=False)

    avg_rating = matrix[matrix.index == id].T.mean()[id]

    ranked_item_score['predicted_rating'] = ranked_item_score['board_score'] + avg_rating
    return ranked_item_score


def groupPredictionWithout(ids: list, jogo):
    dfs = []
    for user in ids:
        dfs.append(predictionWithout(user, jogo))
    groupred = dfs.pop()
    for dataframe in dfs:
        groupred = pd.concat((groupred, dataframe))
    groupred = groupred.groupby(groupred['board'], as_index=False).mean()
    return groupred.sort_values(by='predicted_rating', ascending=False)

def getIndex(ids, jogo):
    pred_id = groupPredictionWithout(ids, jogo)
    print(pred_id.head(10))
    count = 0
    for i in pred_id['board']:
        count += 1
        if i == jogo:
            return count

# print(prediction(20062, 'Gloomhaven'))
ids = [20062, 32761, 58110, 60329]
jogo = 'Gloomhaven'

print(getIndex(ids, jogo))
