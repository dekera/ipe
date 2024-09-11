import math
import numpy as np

# Função para calcular a distância Euclidiana em 3D entre dois pontos
def calcular_distancia(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Função para calcular o vetor direção entre dois nós
def calcular_vetor_direcao(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])

# Função para calcular o produto vetorial entre dois vetores (somente x, y)
def produto_vetorial(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

# Função para calcular o versor (vetor unitário) de um vetor direção
def calcular_versor(vetor):
    norm = np.linalg.norm(vetor)
    return (vetor[0] / norm, vetor[1] / norm) if norm != 0 else (0, 0)