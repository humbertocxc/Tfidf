import math



def knn(X, X_treino, y_treino, k, base):
    dist = {}
    for i in range(len(y_treino)):
        temp = 0
        for i item in X:
            print(i)
        
        temp = math.sqrt(temp)
        dist[temp] = y_treino[i]
    
    for i in sorted(dist):
        base[dist[i]] += 1
        if base[dist[i]] >= k:
            for j in base: base[j] = 0
            return dist[i]



def pega_acerto(X_teste, X_treino, y_teste, y_treino, k, base):
    acerto = 0
    for i in range(len(X_teste)):
        predicao = knn(X_teste[i], X_treino, y_treino, k, base)
        if predicao == y_teste[i]:
            acerto += 1
    
    print(acerto, len(X_teste))
    acerto = acerto/len(X_teste)
    return acerto