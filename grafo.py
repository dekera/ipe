import networkx as nx
from utils import calcular_distancia

# Dicionário para mapear os identificadores dos nós para nomes legíveis
nome_formatado = {
    'guarda': 'Guarda',
    'biblioteca': 'Biblioteca',
    'escada_esquerda_primeiro_piso': 'Escada',
    'elevador_esquerdo_primeiro_piso': 'Elevador',
    'escada_esquerda_quarto_piso': 'Quarto Piso',
    'elevador_esquerdo_quarto_piso': 'Quarto Piso',
    4007: 'Sala 4007',
    4010: 'Sala 4010',
    4013: 'Sala 4013',
    4014: 'Sala 4014',
    'salao_de_honra': 'Salão de Honra',
    'sala_dos_professores': 'Sala dos Professores',
    'auditorio_quarto_piso': 'Auditório - Quarto Piso'
}

# Função para construir o grafo com base na escolha do usuário (escada ou elevador)
def construir_grafo(modo_transporte):
    G = nx.Graph()

    # Coordenadas dos nós (x, y, z)
    posicoes = {
        'guarda': (2, 0, 0),
        'escada_esquerda_primeiro_piso': (1.75, 0.75, 0),
        'elevador_esquerdo_primeiro_piso': (2, 0.75, 0),
        'escada_esquerda_quarto_piso': (1.75, 0.75, 3),
        'elevador_esquerdo_quarto_piso': (2, 0.75, 3),
        4007: (1.125, 0, 3),
        4010: (0.75, 0, 3),
        4013: (0.375, 0, 3),
        4014: (0, 0, 3),
        'biblioteca': (2.5, 0, 3),
        'salao_de_honra': (2, 0, 3),
        'sala_dos_professores': (1.5, 0, 3),
        'auditorio_quarto_piso': (2, 1, 3)
    }# Ao atualizar o grafo precisamos lembrar de atualizar os nome na visualizacao

    # Conectar nós do primeiro andar ao quarto andar
    if modo_transporte == 'escada':
        G.add_edge('guarda', 'escada_esquerda_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['escada_esquerda_primeiro_piso']))
        G.add_edge('escada_esquerda_primeiro_piso', 'escada_esquerda_quarto_piso', weight=calcular_distancia(*posicoes['escada_esquerda_primeiro_piso'], *posicoes['escada_esquerda_quarto_piso']))
    elif modo_transporte == 'elevador':
        G.add_edge('guarda', 'elevador_esquerdo_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['elevador_esquerdo_primeiro_piso']))
        G.add_edge('elevador_esquerdo_primeiro_piso', 'elevador_esquerdo_quarto_piso', weight=calcular_distancia(*posicoes['elevador_esquerdo_primeiro_piso'], *posicoes['elevador_esquerdo_quarto_piso']))

    # Conectar nós do quarto andar com base nas distâncias físicas
    G.add_edge('elevador_esquerdo_quarto_piso', 'salao_de_honra', weight=calcular_distancia(*posicoes['elevador_esquerdo_quarto_piso'], *posicoes['salao_de_honra']))
    G.add_edge('escada_esquerda_quarto_piso', 'salao_de_honra', weight=calcular_distancia(*posicoes['escada_esquerda_quarto_piso'], *posicoes['salao_de_honra']))
    G.add_edge('salao_de_honra', 'sala_dos_professores', weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes['sala_dos_professores']))
    G.add_edge('salao_de_honra', 4007, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4007]))
    G.add_edge('salao_de_honra', 4010, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4010]))
    G.add_edge('salao_de_honra', 4013, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4013]))
    G.add_edge('salao_de_honra', 4014, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4014]))
    G.add_edge('salao_de_honra', 'biblioteca', weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes['biblioteca']))

    # Conectar elevador do quarto andar a outras salas
    G.add_edge('elevador_esquerdo_quarto_piso', 'auditorio_quarto_piso', weight=calcular_distancia(*posicoes['elevador_esquerdo_quarto_piso'], *posicoes['auditorio_quarto_piso']))

    # Conectar as outras salas entre si
    G.add_edge(4013, 4010, weight=calcular_distancia(*posicoes[4013], *posicoes[4010]))
    G.add_edge(4014, 4013, weight=calcular_distancia(*posicoes[4014], *posicoes[4013]))

    return G, posicoes
