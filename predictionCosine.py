import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv', sep=',', names=column_names)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv', sep=',', names=column_names)
df = pd.merge(ratings, board_titles, on='item_id', how='inner')
agg_ratings = df.groupby('title').agg(mean_rating=('rating', 'mean'),
                                      number_of_ratings=('rating', 'count')).reset_index()
agg_ratings_GT100 = agg_ratings[agg_ratings['number_of_ratings'] > 100]
agg_ratings_GT100.sort_values(by='number_of_ratings', ascending=False).head()
df_GT100 = pd.merge(df, agg_ratings_GT100[['title']], on='title', how='inner')
matrix = df_GT100.pivot_table(index='user_id', columns='title', values='rating')

matrix_norm = matrix.subtract(matrix.mean(axis=1), axis='rows')
print(matrix_norm.fillna(0))

def prediction(id):
    print(f'Notas dadas pelo user {id}.')
    print(matrix.iloc[id].dropna(inplace=False))
    user_similarity = cosine_similarity(matrix_norm.fillna(0))

    print('usersim')

    user_similarity_threshold = 0.3

    similar_users = user_similarity[user_similarity[id] > user_similarity_threshold][id].sort_values(
        ascending=False)

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
    print(ranked_item_score.head(5))
    return ranked_item_score


def groupPrediction(ids: list):
    dfs = []
    for user in ids:
        dfs.append(prediction(user))
    groupred = dfs.pop()
    for dataframe in dfs:
        groupred = pd.concat((groupred, dataframe))
    groupred = groupred.groupby(groupred['board']).mean()
    return groupred.sort_values(by='predicted_rating', ascending=False)


# print(groupPrediction([1, 2, 12]).head())
print(prediction(1))