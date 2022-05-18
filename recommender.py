# Imports
import pandas as pd
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")

# conexão por sql
db_connection_str = 'mysql://root:12345678@localhost/recommender' # connection string: "mysql://[connection_name]:[connection_pass]@[hostname]/[database_name]
db_connection = create_engine(db_connection_str)

ratings = pd.read_sql('SELECT * FROM userratings', con=db_connection)
board_titles = pd.read_sql('SELECT * FROM boards', con=db_connection)

# conexão dos CSVs
'''
column_names = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('userratings.csv',sep=',',names=column_names)
column_names = ['item_id', 'title', 'n_players']
board_titles = pd.read_csv('boards.csv',sep=',', names=column_names)
'''

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

def grouprecommender(jogos_e_notas):
    # iniciando variaveis
    n_ratings = 200
    recommenders = []
    soma_notas = 0
    for jogo, nota in jogos_e_notas.items():
        # Faz a recomendação simples e multiplica todas as correlações pela nota do jogo
        recommendation = recommender(jogo, n_ratings)['Correlation'].apply(lambda x: x*nota)
        # Adiciona a recomendação para o vetor do grupo
        recommenders.append(recommendation)
        # Soma as notas
        soma_notas += nota
    # Faz a média das notas
    media = soma_notas / len(recommenders)
    # Adiciona a primeira recomendação a variavel Group
    group = recommenders.pop()
    for df in recommenders:
        # Da merge nas recomendações uma a uma
        group = pd.merge(group, df, how='inner', on='title')
        # Faz a média das recomendações
        group['Correlation'] = group.mean(axis=1)
        group = group['Correlation']
    group = group.to_frame(name='Correlation')
    group = group.sort_values('Correlation', ascending=False)
    # retorna as correlações normalizadas
    return group.apply(lambda x: x/media)


# jogos = {'Zombicide': 10.0, 'Dixit': 10.0, 'Gloomhaven': 8.0, 'Alhambra': 9.0, 'Bandido': 5.0} # string de jogos, "superpessoa"
# print(grouprecommender(jogos, 200).head(10))
