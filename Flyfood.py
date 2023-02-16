# Função que gera todas as possíveis permutações de uma lista fornecida como entrada
def permutacao(l, inicio=0):   
    if inicio == len(l) - 1:
        return [l[:]]
    else:
        saida = []
        for i in range(inicio, len(l)):
            l[inicio], l[i] = l[i], l[inicio]
            saida += permutacao(l, inicio + 1)
            l[inicio], l[i] = l[i], l[inicio]
        return saida
    
# Função para encontrar a melhor rota, recebe as permutações e as coordenadas do arquivo que contém a matriz de entrada  
def melhor_rota(p, c): 
    custo_minimo = float("inf")
    melhor_percuso = []

    for rotas in p: 
        custo_atual = 0
        rotas = ['R'] + rotas + ['R']
        
        for indice_somas in range(len(rotas) - 1): 
            x1, y1 = c[rotas[indice_somas]]
            x2, y2 = c[rotas[indice_somas + 1]]
            custo_atual += abs(x1 - x2) + abs(y1 - y2)
        
        if custo_atual   < custo_minimo:
            custo_minimo = custo_atual
            melhor_percuso  = rotas

    return  melhor_percuso[1:-1], custo_minimo
    
# Abre o arquivo .txt que contém os dados da matriz
arquivo = open('file','r')
m,_ = arquivo.readline().split() 
linhas = arquivo.read().splitlines()   

coordenadas = {}
pontos_entregas = []

# Processa a informação da matriz de entrada, adiciona os pontos de entregas e as coordenadas
for i in range(int(m)):
    m = linhas[i].split()
    for j in m:
        if j != '0':
            coordenadas [j] = (i,m.index(j))
            pontos_entregas.append(j)

pontos_entregas.remove('R') 

# Funçãa (melhor_rota) chama função(permutacao) para calcular o melhor percuso.
percurso = melhor_rota(permutacao(pontos_entregas),coordenadas)  
print(f"{' '.join(percurso[0])}")

