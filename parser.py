import numpy as np


def discountedCumulativeGain(result):
    dcg = []
    for idx, val in enumerate(result):
        numerator = 2**val - 1
        # add 2 because python 0-index
        denominator = np.log2(idx + 2)
        score = numerator/denominator
        dcg.append(score)
    return sum(dcg)

def normalizedDiscountedCumulativeGain(result, sorted_result):
    dcg = discountedCumulativeGain(result)
    idcg = discountedCumulativeGain(sorted_result)
    ndcg = dcg / idcg
    return ndcg

lista = [3, 3, 1, 0, 2, 0, 1, 1, 3]
# print('DCG lista', discountedCumulativeGain(lista))
# print('IDCG lista', discountedCumulativeGain(sorted(lista, reverse=True)))
# print('nDCG lista', normalizedDiscountedCumulativeGain(lista, sorted(lista, reverse=True)))

def nDCG(log):
    results = open(log, 'r', encoding='utf8')
    lines = results.readlines()
    score = []
    for line in lines:
        if 'Score' in line and 'normalization' in line:
            score.append(int(line[-4:-2].strip())+1)
    print(score)
    print(sorted(score, reverse=True))
    print('CG: ', sum(score))
    print('DCG: ', discountedCumulativeGain(score))
    print('nDCG: ', normalizedDiscountedCumulativeGain(score, sorted(score, reverse=True)))

gloomhaven = 'gloom12.txt'
zombicide = 'zombi12.txt'
dixit = 'dixit12.txt'
terramars = 'terra12.txt'

print('IDCG for Gloomhaven')
nDCG(gloomhaven)

print('IDCG for Dixit')
nDCG(dixit)

print('IDCG for Zombicide')
nDCG(zombicide)

print('IDCG for Terraforming Mars')
nDCG(terramars)