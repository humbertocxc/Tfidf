# -*- coding: utf-8 -*-
def le_arq(arq):                                                                                #função que pega um arquivo, cria uma lista e passa cada linha para um ítem da lista
    lista = [line.rstrip() for line in arq]                                                     #transforma o arquivo em uma lista
    arq.close()                                                                                 #fecha o arquivo recebido
    return lista



def remove_stopW(texts, stopW):
    n_texts = []                                                                                #vetor que receberá a nova lista de textos de todos documentos, sem as stopwords
    for d in texts:                                                                             #percorre toda a lista de documentos
        temp = []                                                                               #vetor que receberá o texto do documento d sem as stopwords
        words = d.split(" ")                                                                    #pega todas palavras contidas no texto d
        for w in words:
            if w not in stopW:                                                                  #adiciona ao vetor temp apenas as palavras em d que não estão em stopwords
                temp.append(w)
        temp = " ".join(temp)                                                                   #transforma o temp em um texto com as palavras divididas por um espaço
        n_texts.append(temp)                                                                    #adiciona o vetor temp ao vetor que contém todos os documentos
    
    return n_texts



def aleatoriza(score, texts):
    from random import sample                                                                   #método que cria uma lista aleatória com elementos de outra lista
    sorteados = sample(range(0, len(score)), len(score))                                        #cria uma sequência aleatória, onde cada valor na lista será o índice dos ítens dos vetores s[] e t[] em sua po
    s = []                                                                                      #lista score
    t = []                                                                                      #lista texts
    
    for i in sorteados:                                                                         #percorre lista com posições aleatórias
        temp = score[sorteados[i]]
        s.append(temp)                                                                          #s[i] recebe ítem de score em posição aleatória única
        temp = texts[sorteados[i]]
        t.append(temp)                                                                          #t[i] recebe ítem de texts em mesma posição aleatória única de s
        
    return s, t



def conj_palavra(lista):                                                                        #função que recebe uma lista de documentos e encontra o set de palavras e as palavrasp por documento
    palavra = set()
    docs = []
    for i in lista:
        temp = i.split(" ")                                                                     #separa os ítens do documento divididos por um espaço
        docs.append(temp)                                                                       #conjunto de palavras do documento i
        palavra = palavra.union(set(temp))                                                      #adiciona ao set palavra as possíveis novas palavras em temp
    
    return list(palavra), docs



def pega_base(lista, k):
    if k >= len(lista):                                                                         #garante que número de pastas é menor que o número de documentos
        k = int(len(lista)*0.2)
    if k < 2:                                                                                   #garante que número de pastas é maior que 1
        k = 2

    base, docs = conj_palavra(lista)                                                            #função que pega todos tipos de ítens contidos em

    dicionario = dict.fromkeys(base, 0)
    for word in lista:
        dicionario[word] += 1                                                                   #pega o total de ítems com cada tipo de resultado

    for word in base:
        dicionario[word] = int(dicionario[word]/k)                                              #pega a quantidade desses ítens que terão em cada pasta
                                                                                                #dividindo a quantidade de ítens por k, qu eé o número de pastas
    return dicionario, k



def separa_lista(texts, score, k, base):                                                        #função que recebe uma lista, a proporção do tamanho do treino e divide em duas listas, uma de treino e uma de teste
    X = [list() for _ in range(k)]                                                              #lista que contém k listas, cada sublista com um dos k grupos de X
    y = [list() for _ in range(k)]                                                              #lista que contém k listas, cada sublista com um dos k grupos de y
    tipos = []
    qt = []
    compara = []
    pos = []

    for word in base:
        tipos.append(word)                                                                      #tipos é uma lista que contém os 'word' diferentes ítens contidos na base
        qt.append(base.get(word))                                                               #qt é uma lista que contém a quantidade de cada ítem contido na base
        compara.append(0)                                                                       #lista que vai contar, para cada ítem na base, a quantidade adicionada ao grupo atual
        pos.append(0)                                                                           #lista que indica em qual grupo deve ser adicionado cada ítem da base

    for i in range(len(score)):                                                                 #percorre a lista score
        val = tipos.index(score[i])                                                             #val recebe o tipo de ítem contido em score[i]
        if compara[val] >= qt[val]:                                                             #se compara na posição val ultrapassar o máximo(qt), o ítem score[i] e seus semelhantes
            pos[val] += 1                                                                       #serão adicionados ao próximo grupo, aumentando a pos[val] em 1
            if pos[val] >= k:                                                                   
                pos[val] = k-1                                                                  #caso o grupo pos[val] chegue à posição k, ele volta para a posição k-1, que é o último grupo
            compara[val] = 0                                                                    #zera o compara para o ítem score[i]
        X[pos[val]].append(texts[i])                                                            #X no grupo pos[val] recebe texts[i]
        y[pos[val]].append(score[i])                                                            #y no grupo pos[val] recebe score[i]
        compara[val] += 1                                                                       #soma 1 na compara[val], pois um novo ítem do tipo val foi adicionado nesse grupo
    
    return X, y



def divide_t(lista, pos, k):                                                                    #função que une os k grupos, escolhe um para teste e o restante para o treino
    treino = []
    teste = []
    for i in range(k):                                                                          #percorre os k grupos
        if i != pos:                                                                            #pos é uma variável que indica a posição do grupo de teste atual
            treino.extend(lista[i])                                                             #se i for diferente de pos, significa que lista[i] será incluída em treino
        else:
            teste.extend(lista[i])                                                              #quando i for igual a pos, lista[i] é o teste
    return treino, teste



def pega_termos_treino(X):
    word_dict = []                                                                              #lista que contém o número de aparições de cada palavra do conjunto para cada documento

    word_set, docs_words = conj_palavra(X)                                                      #função que pega as palavras existentes em X, além das palavras contidas em cada documento

    for i in range(len(X)):
        temp = dict.fromkeys(word_set, 0)                                                       #cria dicionário contendo todas palavras do word_set, com número de aparições igual a 0 para todas elas
        for word in docs_words[i]:                                                              #percorre todas palavras contidas no documento i e soma 1 no número de aparições de cada uma
            temp[word] += 1
        word_dict.append(temp)                                                                  #adiciona o novo dicionário à lista word_dict

    return docs_words, word_set, word_dict



def pega_termos_test(X, word_set):
    docs_words = []                                                                             #lista que contém as palavras contidas em cada documento
    word_dict = []                                                                              #lista que contém o número de aparições de cada palavra do conjunto para cada documento
    i = 0
    for i in X:                                                                                 #percorre todo o conjunto de treino
        temp = i.split(" ")                                                                     #separa a string do documento em uma lista de palavras
        temp = list(set(temp).intersection(set(word_set)))                                      #pega interseção dos ítens em temp com o word_set do treino
        docs_words.append(temp)                                                                 #adiciona a lista à lista docs_words
    
    for i in range(len(X)):
        temp = dict.fromkeys(word_set, 0)                                                       #cria dicionário contendo todas palavras do word_set, com número de aparições igual a 0 para todas elas
        for word in docs_words[i]:                                                              #percorre todas palavras contidas no documento i e soma 1 no número de aparições de cada uma
            temp[word] += 1
        word_dict.append(temp)                                                                  #adiciona o novo dicionário à lista word_dict

    return docs_words, word_dict



def executa_treino_teste(X, y, k, base):
    from tfidf.manual import cria_matriz_treino, cria_matriz_teste                              #funções que criam matriz tfidf para treion e teste
    from knn.knn import pega_acerto

    media = 0
    
    for i in range(k):
        X_train, X_test = divide_t(X, i, k)                                                     #pega uma pasta do fold cross validation para o teste e o restante para o treino na lista X
        y_train, y_test = divide_t(y, i, k)                                                     #pega uma pasta do fold cross validation para o teste e o restante para o treino na lista y

        docs_words, word_set, word_dict = pega_termos_treino(X_train)                           #função que encontra as frases em palavras, cria word_set que contém o conjunto de palavras, docs_words que contém as palavras em cada frase e word_dict que contém o número de aparição de cada palavra em cada frase
        docs_words_test, word_dict_test = pega_termos_test(X_test, word_set)                    #pega dicionário e palavras do teste, com base nas palavras encontradas no treino

        matriz_treino, idf = cria_matriz_treino(docs_words, word_dict, word_set)                #função que cria a matriz TFIDF para o treino
        matriz_teste = cria_matriz_teste(docs_words_test, word_dict_test, word_set, idf)        #função que cria a matriz TFIDF para o teste, usando o IDF da matriz treino

        acuracia = pega_acerto(matriz_teste, matriz_treino, y_train, y_test, 5, base)
        media += acuracia
    
    media /= k
    print("Acerto médio do KNN foi", media)



def treino_teste_lib(X, y, k, base):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    # from knn.knn_l import pega_acerto
    media = 0
    
    for i in range(1):
        X_train, X_test = divide_t(X, i, k)                                                     #pega uma pasta do fold cross validation para o teste e o restante para o treino na lista X
        y_train, y_test = divide_t(y, i, k)                                                     #pega uma pasta do fold cross validation para o teste e o restante para o treino na lista y

        tf = TfidfVectorizer()

        tf = tf.fit(X_train) #configura baseado nos termos do treino

        matriz_treino = tf.transform(X_train) #transforma em matriz
        matriz_teste = tf.transform(X_test)

        matriz_teste.toarray()

        print(type(matriz_teste))

        # acuracia = pega_acerto(matriz_teste, matriz_treino, y_train, y_test, 5, base)
        # media += acuracia
    
    media /= k
    print("Acerto médio do KNN foi", media)
        


def printa_matriz(matriz, word_set):
    for i in range(len(matriz)):                                                                #percorre todos os documentos
        print("\nDocumento número ", i+1)
        for j in range(len(word_set)):                                                          #percorre todas as palavras
            if(matriz[i][j] > 0):
                print(matriz[i][j], "\t----\t", word_set[j])                                    #quando o tfidf da palavra j no documento i é maior que zero, escreve ele