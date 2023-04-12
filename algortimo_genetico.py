import random
from random import randint, random, shuffle
from typing import Tuple, List
from math import cos, radians, factorial


"""
Algoritmo Genético para o problema do caxeiro viajante, sem elitismo e utilizando o
  operador de crossover pmx.

OBS: os dados de entrada do Algoritmo está na linha 154. 
"""

# Função que gera a população inicial do algoritmo
def inicializacao(arr: List[Tuple], n_individual: int) -> List[list]:     
    mistura_pontos = []
    while len(mistura_pontos) < n_individual:
        permut_geracao = arr[:]
        shuffle(permut_geracao)
        if permut_geracao not in mistura_pontos:
            mistura_pontos.append(permut_geracao)           
    return mistura_pontos

# Função que calcula a distância de todas as rotas em uma lista, utilizando distância de Manhattan
def calc_distancia(lista_cidade: List[object]) -> List[float]:
  calc_rotas = [' '] * len(lista_cidade)
  for ind, r in enumerate(lista_cidade):
    distancia_manhattan = (abs(r[0][0] - r[1][0]) + abs(r[0][1] - r[1][1]))
    for index, caminho in enumerate(r[1:]):
      if index != len(r)-2:
        distancia_manhattan += (abs(caminho[0] - r[index + 2][0]) + abs(caminho[1] - r[index + 2][1]))
    distancia_manhattan += (abs(r[-1][0] - r[0][0]) + abs(r[-1][1] - r[0][1]))
    calc_rotas[ind] = distancia_manhattan
  return calc_rotas

# Função que sorteia 2 individuos aleatoriamente e os compara, retornando o com maior aptidão, chamada na função selecionar_pais e evolucao
def sel_torneio(apt: List[float]) -> int:
    pai1 = randint(0, len(apt) - 1)
    pai2 = randint(0, len(apt) - 1)
    return pai1 if apt[pai1] > apt[pai2] else pai2

def sel_roleta(apt: List[float]) -> int:
    soma_roleta: float = sum(apt)
    n_sorteado: float = random() * soma_roleta
    soma_atual: float = 0
    for i, apt in enumerate(apt):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            return i

# Função que calcula a apitidão (fitness) dos indivíduos, com list comprehension,  multiplica por pi/2 para deixar no intervalo de 0 a 1:
def avaliacao(pop_list: List[float]) -> List[float]:
    return [cos(el*radians(90)) for el in pop_list]

#Função de cruzamento de genes
def op_crossover_pmx(pai1, pai2):
    ponto_corte1 = randint(0, len(pai1) - 1)
    ponto_corte2 = randint(0, len(pai1) - 1)
    ponto_corte1, ponto_corte2 = min(ponto_corte1, ponto_corte2), max(ponto_corte1, ponto_corte2)

    filhos = pai1[:]

    for i in range(ponto_corte1, ponto_corte2):
        if pai2[i] not in filhos[ponto_corte1:ponto_corte2]:
            j = pai1.index(pai2[i])
            filhos[i], filhos[j] = filhos[j], filhos[i]

    for i in range(ponto_corte1, ponto_corte2):
        if pai2[i] not in filhos[ponto_corte1:ponto_corte2]:
            j = pai1.index(pai2[i])
            filhos[j], filhos[i] = filhos[i], filhos[j]

    return filhos


# Decide aleatoriamente se deve ou não realizar o crossover (com base na taxa de crossover)
def tx_cruzamento(pai1: List[object], pai2: List[object], crossover_rate: float)-> Tuple[list, list] :
  if random() < crossover_rate:
    return op_crossover_pmx(pai1, pai2), op_crossover_pmx(pai2, pai1)
  return pai1, pai2

def crossover(pais_list: List[List[object]], crossover_rate: float) -> List[List[object]]:
    filhos_list = []
    for pai1, pai2 in zip(pais_list[::2], pais_list[1::2]):
        son1, son2 = tx_cruzamento(pai1, pai2, crossover_rate)
        filhos_list.extend([son1, son2])
    return filhos_list

# Função que seleciona um pai   
def selecionar_pais(pop_list: List[List[object]], distancias: List[float], sel_func):
  min_val = min(distancias)
  max_val = max(distancias)
  escala_lst = [(x - min_val +1) / (max_val - min_val +1) for x in distancias]
  fitness_list = avaliacao(escala_lst)
  pais_list = [' '] * len(pop_list)
  for count in range(0, len(pais_list), 2):
    pai1 = sel_func(fitness_list)
    pai2 = sel_func(fitness_list[:pai1]+fitness_list[pai1+1:])
    pais_list[count],pais_list[count+1] = pop_list[pai1], pop_list[pai2]
  return pais_list

# Função de mutação de genes
def mutacao(pop_list: List[List[object]], mutation_rate: float):
  for i, el in enumerate(pop_list):
    if random() <= mutation_rate:
      a = randint(0, len(el)-1)
      b = randint(0, len(el)-1)
      pop_list[i][a], pop_list[i][b] = pop_list[i][b], pop_list[i][a]
  return pop_list

# Função de evolução que cuida de controlar todas as gerações
def evolucao(
  data: List[object], n_individuos : int, quant_generacaoes : int, 
  crossover_rate: float, mutation_rate: float, sel_func
) -> Tuple[List[List[object]], List[float]]:
  
  populacao_inicial = inicializacao(data, n_individuos )
  
  for generation in range(quant_generacaoes ):
    distancias = calc_distancia(populacao_inicial)
    melhor_individuo = distancias[distancias.index(min(distancias))]
    parents = selecionar_pais(populacao_inicial, distancias, sel_func)
    filhos = crossover(parents, crossover_rate)
    mutated_filhos = mutacao(filhos, mutation_rate)
    populacao_inicial = mutated_filhos[:]
    print(f'Geração: {generation+1}º:-> Distância: {melhor_individuo}')
    for count, tuplas in enumerate(populacao_inicial):
        print(f'Caminho {count+1}:', end=' ')
        for tupla in tuplas:
            ultimo_valor = tupla[-1]
            print(ultimo_valor, end=' ')
        
        print() 
        best_route = mutated_filhos[distancias.index(min(distancias))]
    print('Melhor Rota: ',*(c[-1] for c in best_route),'-> Distância:', melhor_individuo)
    print()
  return populacao_inicial, distancias


# leitura do arquivo 
with open('teste.txt') as file:
    text = file.readlines()

lista = [((int(x[1])), (int(x[2])), str(x[0])) for x in (line.replace('\n', ' ').split() for line in text[:-1]) if x]

# Entrada dos dados do Algoritmo
evolucao(
  data= lista,
  n_individuos = 20,
  quant_generacaoes = 50, 
  crossover_rate = 0.8,  
  mutation_rate = 0.1, 
  sel_func=sel_roleta # sel_roleta ou sel_torneio
)