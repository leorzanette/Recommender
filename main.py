import recommender

jogos_notas = {}
jogadores = []
x = True
y = True
while x:
    jogador = input('Qual o nome do jogador? Digite 0 para sair.')
    y = True
    if jogador == '0':
        x = False
    else:
        jogadores.append(jogador)
        while y:
            jogo = input('Qual o nome do jogo? Digite 0 para sair.')
            if jogo == '0':
                y = False
            else:
                nota = int(input('Qual nota você dá ao jogo?'))
                if jogo in jogos_notas:
                    notinha = jogos_notas[jogo]
                    jogos_notas[jogo] = (notinha + nota)/2
                else:
                    jogos_notas[jogo] = nota

print(recommender.grouprecommender(jogos_notas).head(10))