import pandas as pd

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


def prediction(id):
    user_similarity = matrix_norm.T.corr()
    # print(user_similarity)
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


id = 2

# print(groupPrediction([1, 2, 12]).head())
print(prediction(id).head())


print(f'Notas dadas pelo user {id}.')
notas_id = matrix.iloc[id].dropna(inplace=False)
print(notas_id)

media_notas_id = 0
notas_id_count = 0
for k, v in notas_id.items():
    media_notas_id += v
    notas_id_count += 1
print(f'Média do user {id}: {media_notas_id/notas_id_count}')

pred_id = prediction(id)
falso_positivo = 0
falso_negativo = 0
verdadeiro_positivo = 0
verdadeiro_negativo = 0
divisor = 7
for k, v in notas_id.items():
    print(f'{k}: {v}')
    correlacao = float(pred_id.loc[pred_id['board'] == k]['board_score'])
    nota_predita = float(pred_id.loc[pred_id['board'] == k]['predicted_rating'])
    print(f'Nota predita: {nota_predita:.2f}.'
          f'Correlação: {correlacao:.5f}')
    if nota_predita > divisor and v > divisor:
        verdadeiro_positivo += 1
    elif nota_predita > divisor and v < divisor:
        falso_positivo += 1
    elif nota_predita < divisor and v < divisor:
        verdadeiro_negativo += 1
    elif nota_predita < divisor and v > divisor:
        falso_negativo += 1

print(f'Verdadeiros positivos: {verdadeiro_positivo}')
print(f'Falsos positivos: {falso_positivo}')
print(f'Verdadeiros negativos: {verdadeiro_negativo}')
print(f'Falsos negativos: {falso_negativo}')
precision = verdadeiro_positivo/(verdadeiro_positivo+falso_positivo)
print(f'Precision: {precision}')
