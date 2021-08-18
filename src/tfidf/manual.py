def computa_TF(word_dict, word_set, docs_words):
    matriz_tf = []                                                                              #matriz que receberá frequência dos termpos por documento
    for i in range(len(docs_words)):                                                            #percorre todos os documentos
        linha = []                                                                              #lista que receberá os ítens de uma linha da matriz
        tam = float(len(docs_words[i])) + 0.000001                                              #variável que armazena o total de palavras no documento i
        for j in range(len(word_set)):                                                          #percorre lista com todas palavras
            qt = word_dict[i].get(word_set[j])                                                  #pega quantidade de vezes que a palavra j aparece no documento i
            num = qt/tam
            linha.append(num)                                                                   #pega razão entre qt e tam e adiciona à lista linha
        matriz_tf.append(linha)                                                                 #adiciona a linha com frequência da palavra j em todos documentos à matriz
    
    return matriz_tf
    


def computa_IDF(word_dict, word_set, docs_words):
    import math                                                                                 #biblioteca necessária para utilizar o log
    idf = []

    i = 0
    for word in range(len(word_set)):                                                           #percorre todas as palavras
        den = 0                                                                                 #variável que conterá o denominador da palavra i
        for j in range(len(docs_words)):                                                        #percorre todos os documentos
            if word_set[i] in docs_words[j]:
                den += 1                                                                        #para cada documento que contém a palavra, o denominador aumenta em 1
        if den < 2 or den >= len(docs_words):                                                   #quando a palavra for "inútil" é removida do word_set e do vetor idf
            word_set.remove(word_set[i])
        else:
            idf.append(den)
            i += 1

    num = len(word_dict)                                                                        #numerador das palavras será o número de documentos

    for i in range(len(word_set)):
        idf[i] = math.log10(num/float(idf[i]+0.00000001)+0.00000001)                            #para cada palavra, pega o numerador, divide pelo valor inicial que era o denominador e encontra o log10 da razão
    
    return idf, word_set, word_dict
    


def cria_matriz_treino(docs_words, word_dict, word_set):
    idf, word_set, word_dict = computa_IDF(word_dict, word_set, docs_words)                     #função que cria uma lista que contém o idf, com base no número de aparições de cada palavra nos documentos
    matriz = computa_TF(word_dict, word_set, docs_words)                                        #função que cria uma matriz que contém as frequências do conjunto de palavras em cada documento

    for i in range(len(word_dict)):                                                             #percorre todos os documentos
        for j in range(len(word_set)):                                                          #percorre todas as palavras
            matriz[i][j] = matriz[i][j] * idf[j]                                                #para todas palavras na matriz em i, multiplica os valores de tf pelo idf

    return matriz, idf



def cria_matriz_teste(docs_words, word_dict, word_set, idf):
    matriz = computa_TF(word_dict, word_set, docs_words)                                        #função que cria uma matriz que contém as frequências do conjunto de palavras em cada documento

    for i in range(len(word_dict)):                                                             #percorre todos os documentos
        for j in range(len(word_set)):                                                          #percorre todas as palavras
            matriz[i][j] = matriz[i][j] * idf[j]                                                #para todas palavras na matriz em i, multiplica os valores de tf pelo idf

    return matriz