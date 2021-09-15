# -*- coding: utf-8 -*-
from funcs import le_arq, aleatoriza, pega_base, separa_lista, executa_treino_teste, remove_stopW, treino_teste_lib
import sys
import time



inicio = time.time()

score = le_arq(open(sys.argv[1], 'r'))                                                          #chama função le_arq, que lê cada linha do arquivo e passa para uma lista
texts = le_arq(open(sys.argv[2], 'r'))                                                          #chama função le_arq, que lê cada linha do arquivo e passa para uma lista
stopW = le_arq(open(sys.argv[3], 'r'))                                                          #chama função le_arq, que lê cada linha do arquivo e passa para uma lista

texts = remove_stopW(texts, stopW)

score, texts = aleatoriza(score, texts)

k = 5                                                                                           #número de pastas do k cross validation
base, k = pega_base(score, k)                                                                   #função que pega a quantidade de tipos de resposta no y em cada pasta do k cross validation
X, y = separa_lista(texts, score, k, base)                                                      #função que separa as listas X e y em k pastas, com as mesmas proporções entre os resultados


for i in base:
    base[i] = 0

#executa_treino_teste(X, y, k, base)                                                             #função que gera os diferentes treinos e testes, com base nas k pastas criadas para X e y, para melhor precisão na execução do knn
treino_teste_lib(X, y, k, base)



fim = time.time()
print("\n\n\nTempo de execução =", fim - inicio, "segundos.\n")