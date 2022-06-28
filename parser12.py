def teste(log):
    print(log)
    results = open(log, 'r', encoding='utf8')
    lines = results.readlines()
    score = []
    for line in lines:
        if 'Score' in line and 'normalization' in line:
            score.append(int(line[-4:-2].strip())+1)
    # print(score)
    print('CG: ', sum(score))

    from parser import nDCG

    nDCG(log)
    return

teste('gloom12.txt')
teste('terra12.txt')
teste('dixit12.txt')
teste('zombi12.txt')