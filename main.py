# Imports
import pandas as pd
from IPython.display import display
from sqlalchemy import create_engine

# conexão por sql
'''db_connection_str = 'mysql://root:12345678@localhost/recommender' # connection string: "mysql://[connection_name]:[connection_pass]@[hostname]/[database_name]
db_connection = create_engine(db_connection_str)

ratings = pd.read_sql('SELECT * FROM userratings', con=db_connection)
board_titles = pd.read_sql('SELECT * FROM boards', con=db_connection)
'''
# conexão dos CSVs
column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv',sep=',',names=column_names)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv',sep=',', names=column_names)


ratings = pd.merge(ratings, board_titles, on='item_id')
ratings.groupby('title')['rating'].mean()
ratings.groupby('title')['rating'].mean().sort_values(ascending=False).head()
ratings_df = pd.DataFrame(ratings.groupby('title')['rating'].mean())
ratings_df.rename(columns={'rating': 'average_rating'}, inplace=True)
ratings_df['num_of_ratings'] = pd.DataFrame(ratings.groupby('title')['rating'].count())

# Criando o recommender
user_board_matrix = ratings.pivot_table(values='rating', index='user_id', columns='title')


def recommender(board_x, min_num_reviews):
    # Guarda os user ratings do board em uma variável
    board_x_user_ratings = user_board_matrix[board_x]
    # Cria uma serie de relações entre todos os boards e o board_x usando pandas
    similar_to_board_x = user_board_matrix.corrwith(board_x_user_ratings)
    # Converte para um dataframe
    corr_board_x = pd.DataFrame(similar_to_board_x, columns=['Correlation'])
    # Exclui os valores nulos
    corr_board_x.dropna(inplace=True)
    # Da join nas informações dos ratings e habilita o filtro para os boards com poucos ratings
    corr_board_x = corr_board_x.join(ratings_df['num_of_ratings'])
    # Aplica o filtro
    new_corr_board_x = corr_board_x[corr_board_x['num_of_ratings'] >= min_num_reviews]
    # Da sort nos ratings em ordem ascendente e retorna o dataframe
    return new_corr_board_x.sort_values('Correlation', ascending=False)


def grouprecommender(jogos_e_notas, n_ratings):
    dfs = []
    for k,v in jogos_e_notas.items():
        dfp = recommender(k, n_ratings)['Correlation'].apply(lambda x: x*v)
        dfs.append(dfp)
    df_final = dfs.pop()
    for df in dfs:
        df_final = pd.merge(df_final, df, how='inner', on='title')
        df_final['Correlation'] = df_final.mean(axis=1)
        df_final = df_final['Correlation']
    df_final = df_final.to_frame(name='Correlation')
    df_final = df_final.sort_values('Correlation', ascending=False)
    return df_final


jogos = {'Zombicide': 8.0, 'Dixit': 3.0, 'Gloomhaven': 1.0, 'Alhambra': 6.0, 'Bandido': 8.0} # string de jogos, "superpessoa"
display(grouprecommender(jogos, 200).head(10))

#print(recommender('Dixit', 350).head(5))
