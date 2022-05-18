import pandas as pd
from sqlalchemy import create_engine

db_connection_str = 'mysql://root:12345678@localhost/recommender'
db_connection = create_engine(db_connection_str)

ratings = pd.read_sql('SELECT * FROM userratings', con=db_connection)
board_titles = pd.read_sql('SELECT * FROM boards', con=db_connection)
print("Tabela ratings, colunas são: id do user, id do jogo e sua nota: ")
print(ratings.head(10))
print("---------------------------")
print("Tabela boards, id do jogo, nome do jogo e numero de jogadores: ")
print(board_titles.head(10))
print("---------------------------")

ratings = pd.merge(ratings, board_titles, on='item_id')
print("Merge das tabelas boards e ratings: ")
print(ratings.head(10))
print("---------------------------")

ratings.groupby('title')['rating'].mean()
ratings.groupby('title')['rating'].mean().sort_values(ascending=False).head()
ratings_df = pd.DataFrame(ratings.groupby('title')['rating'].mean())
print("RatingsDF consiste no merge das tabelas, agrupado por titulo, feito a média das notas: ")
print(ratings_df.head(10))
print("---------------------------")

ratings_df.rename(columns={'rating': 'average_rating'}, inplace=True)
print("RatingsDF coluna rating renomeada para average_rating: ")
print(ratings_df.head((10)))
print("---------------------------")

ratings_df['num_of_ratings'] = pd.DataFrame(ratings.groupby('title')['rating'].count())
print("RatingsDF numero de ratings de cada jogo: ")
print(ratings_df['num_of_ratings'].head(10))
print("---------------------------")

# Criando o recommender
user_board_matrix = ratings.pivot_table(values='rating', index='user_id', columns='title')
print("User board matrix que consiste em ratings pivoteado usando user_id como linhas, title como colunas e nota como valores: ")
print(user_board_matrix.head(10))
print("---------------------------")

board_x = "Gloomhaven"
min_num_reviews = 250

board_x_user_ratings = user_board_matrix[board_x]
print("Ratings do board game Gloomhaven: ")
similar_to_gloomhaven = board_x_user_ratings.dropna()
print(similar_to_gloomhaven.head(10))
print("---------------------------")

similar_to_board_x = user_board_matrix.corrwith(board_x_user_ratings)
print("Correlação de todos os jogos com o jogo Gloomhaven: ")
print(similar_to_board_x.head(10))
print("---------------------------")

corr_board_x = pd.DataFrame(similar_to_board_x, columns=['Correlation'])
print("Coluna de correlações renomeada: ")
print(corr_board_x.head(10))
print("---------------------------")

corr_board_x.dropna(inplace=True)
print("Filtrados valores sem correlação: ")
print(corr_board_x.head(10))
print("---------------------------")

corr_board_x = corr_board_x.join(ratings_df['num_of_ratings'])
print("dataframe das correlações joinado com o numero de ratings: ")
print(corr_board_x.head(10))
print("---------------------------")

new_corr_board_x = corr_board_x[corr_board_x['num_of_ratings'] >= min_num_reviews]
print("filtrado para aparecer apenas numeros de ratings maiores que 250(jogos um pouco mais populares): ")
print(new_corr_board_x.head(10))
print("---------------------------")
new_corr_board_x = new_corr_board_x.sort_values('Correlation', ascending=False)
print("Ordenado por correlação mais alta")
print(new_corr_board_x.head(10))
