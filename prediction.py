import pandas as pd
column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv', sep=',', names=column_names)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv',sep=',', names=column_names)
df = pd.merge(ratings, board_titles, on='item_id', how='inner')
agg_ratings = df.groupby('title').agg(mean_rating=('rating', 'mean'),
                                      number_of_ratings=('rating', 'count')).reset_index()
agg_ratings_GT100 = agg_ratings[agg_ratings['number_of_ratings'] > 100]
agg_ratings_GT100.sort_values(by='number_of_ratings', ascending=False).head()
df_GT100 = pd.merge(df, agg_ratings_GT100[['title']], on='title', how='inner')
matrix = df_GT100.pivot_table(index='user_id', columns='title', values='rating')
matrix_norm = matrix.subtract(matrix.mean(axis=1), axis='rows')
user_similarity = matrix_norm.T.corr()

picked_userid = 12
n = 10
user_similarity_threshold = 0.3

similar_users = user_similarity[user_similarity[picked_userid] > user_similarity_threshold][picked_userid].sort_values(
    ascending=False)[:n]

picked_userid_played = matrix_norm[matrix_norm.index == picked_userid].dropna(axis=1, how='all')
similar_user_boards = matrix_norm[matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
similar_user_boards.drop(picked_userid_played.columns, axis=1, inplace=True, errors='ignore')
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

m = 10
ranked_item_score.head(m)

avg_rating = matrix[matrix.index == picked_userid].T.mean()[picked_userid]

ranked_item_score['predicted_rating'] = ranked_item_score['board_score'] + avg_rating

ranked_item_score.head(m)
