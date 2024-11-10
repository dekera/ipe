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
    'sala_mecanica' :'Sala Mecânica',
    'esquinae4': 'Esquina',
    'salao_de_honra': 'Salão de Honra',
    'sala_dos_professores': 'Sala dos Professores',
    'auditorio_quarto_piso': 'Auditório - Quarto Piso',
    'salao_de_estudos': 'Sala de Estudos'
}

# Função para construir o grafo com base na escolha do usuário (escada ou elevador)
def construir_grafo(modo_transporte):
    G = nx.Graph()

    # Coordenadas dos nós (x, y, z)
    posicoes = {
        'guarda': (520, 580, 0),
        'esquinae1': (250,580,0),
        'div_de_telematica':(537, 580,0),
        'dep_eng_mec_mat':(260, 580,0),
        'auditorio_se8':(237, 524,0),
        'escada_esquerda_primeiro_piso': (510, 550, 0),
        'elevador_esquerdo_primeiro_piso': (514, 527, 0),
        'escada_esquerda_quarto_piso': (510,  550, 3),
        'elevador_esquerdo_quarto_piso': (514, 527, 3),
        4007: (380, 580, 3),
        4010: (300, 580, 3),
        4013: (260, 580, 3),
        4014: (215, 580, 3),
        'esquinae4': (250, 580, 3),
        'esquinae1': (250,580,0),
        'biblioteca': (650, 580, 3),
        'salao_de_honra': (537, 580, 3),
        'salao_de_estudos': (537, 580, 3),
        'sala_dos_professores': (465, 580, 3),
        'sala_mecanica': (237,524,3),
        'auditorio_quarto_piso': (537, 510, 3)
    }# Ao atualizar o grafo precisamos lembrar de atualizar os nome na visualizacao

    # Conectar nós do primeiro andar aos outros andares
    if modo_transporte == 'Escada':
        G.add_edge('guarda', 'escada_esquerda_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['escada_esquerda_primeiro_piso']))
        G.add_edge('escada_esquerda_primeiro_piso', 'escada_esquerda_quarto_piso', weight=calcular_distancia(*posicoes['escada_esquerda_primeiro_piso'], *posicoes['escada_esquerda_quarto_piso']))
    elif modo_transporte == 'Elevador':
        G.add_edge('guarda', 'elevador_esquerdo_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['elevador_esquerdo_primeiro_piso']))
        G.add_edge('elevador_esquerdo_primeiro_piso', 'elevador_esquerdo_quarto_piso', weight=calcular_distancia(*posicoes['elevador_esquerdo_primeiro_piso'], *posicoes['elevador_esquerdo_quarto_piso']))

    # Conectar nós do primeiro andar com base nas distâncias físicas
    G.add_edge('guarda', 'esquinae1', weight=calcular_distancia(*posicoes['guarda'], *posicoes['esquinae1']))
    G.add_edge('guarda', 'div_de_telematica', weight=calcular_distancia(*posicoes['guarda'], *posicoes['div_de_telematica']))
    G.add_edge('guarda', 'dep_eng_mec_mat', weight=calcular_distancia(*posicoes['guarda'], *posicoes['dep_eng_mec_mat']))
    G.add_edge('esquinae1', 'auditorio_se8', weight=calcular_distancia(*posicoes['esquinae1'], *posicoes['auditorio_se8']))

    # Conectar nós do quarto andar com base nas distâncias físicas
    G.add_edge('elevador_esquerdo_quarto_piso', 'salao_de_honra', weight=calcular_distancia(*posicoes['elevador_esquerdo_quarto_piso'], *posicoes['salao_de_honra']))
    G.add_edge('escada_esquerda_quarto_piso', 'salao_de_honra', weight=calcular_distancia(*posicoes['escada_esquerda_quarto_piso'], *posicoes['salao_de_honra']))
    G.add_edge('salao_de_honra', 'sala_dos_professores', weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes['sala_dos_professores']))
    G.add_edge('salao_de_honra', 4007, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4007]))
    G.add_edge('salao_de_honra', 4010, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4010]))
    G.add_edge('salao_de_honra', 4013, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4013]))
    G.add_edge('salao_de_honra', 4014, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4014]))
    G.add_edge('esquinae4', 'salao_de_honra', weight=calcular_distancia(*posicoes['esquinae4'], *posicoes['salao_de_honra']))
    G.add_edge('esquinae4', 'sala_mecanica', weight=calcular_distancia(*posicoes['esquinae4'], *posicoes['sala_mecanica']))
    G.add_edge('salao_de_honra', 'biblioteca', weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes['biblioteca']))

    # Conectar elevador do quarto andar a outras salas
    G.add_edge('elevador_esquerdo_quarto_piso', 'auditorio_quarto_piso', weight=calcular_distancia(*posicoes['elevador_esquerdo_quarto_piso'], *posicoes['auditorio_quarto_piso']))

    # Conectar as outras salas entre si
    G.add_edge(4013, 4010, weight=calcular_distancia(*posicoes[4013], *posicoes[4010]))
    G.add_edge(4014, 4013, weight=calcular_distancia(*posicoes[4014], *posicoes[4013]))

    return G, posicoes