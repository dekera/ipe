import math
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sqlite3
from PyQt5 import uic, QtWidgets

# Função para calcular a distância Euclidiana em 3D entre dois pontos
def calcular_distancia(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Função para construir o grafo com base na escolha do usuário (escada ou elevador)
def construir_grafo(modo_transporte):
    G = nx.Graph()

    # Coordenadas dos nós (x, y, z)
    posicoes = {
        'guarda': (2, 0, 0),                           
        'escada_esquerda_primeiro_piso': (1.75, 0.75, 0),             
        'elevador_esquerdo_primeiro_piso': (1.8, 0.75, 0),
        'escada_esquerda_quarto_piso': (1.75, 0.75, 3),
        'elevador_quarto_piso': (1.8, 0.75, 3),
        4007: (1.25, 0, 3),
        4010: (1, 0, 3),
        4013: (0.5, 0, 3),
        4014: (0, 0, 3),
        'salao_de_honra': (2, 0, 3),
        'sala_dos_professores': (1.5, 0, 3),
        'auditorio_quarto_piso': (2, 1, 3)
    }

    # Conectar nós do primeiro andar ao quarto andar
    if modo_transporte == 'escada':
        G.add_edge('guarda', 'escada_esquerda_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['escada_esquerda_primeiro_piso']))
        G.add_edge('escada_esquerda_primeiro_piso', 'escada_esquerda_quarto_piso', weight=calcular_distancia(*posicoes['escada_esquerda_primeiro_piso'], *posicoes['escada_esquerda_quarto_piso']))
    elif modo_transporte == 'elevador':
        G.add_edge('guarda', 'elevador_esquerdo_primeiro_piso', weight=calcular_distancia(*posicoes['guarda'], *posicoes['elevador_esquerdo_primeiro_piso']))
        G.add_edge('elevador_esquerdo_primeiro_piso', 'elevador_quarto_piso', weight=calcular_distancia(*posicoes['elevador_esquerdo_primeiro_piso'], *posicoes['elevador_quarto_piso']))

    # Conectar nós do quarto andar com base nas distâncias físicas
    G.add_edge('escada_esquerda_quarto_piso', 'salao_de_honra', weight=calcular_distancia(*posicoes['escada_esquerda_quarto_piso'], *posicoes['salao_de_honra']))
    G.add_edge('salao_de_honra', 'sala_dos_professores', weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes['sala_dos_professores']))
    G.add_edge('salao_de_honra', 4007, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4007]))
    G.add_edge('salao_de_honra', 4010, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4010]))
    G.add_edge('salao_de_honra', 4013, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4013]))
    G.add_edge('salao_de_honra', 4014, weight=calcular_distancia(*posicoes['salao_de_honra'], *posicoes[4014]))

    # Conectar elevador do quarto andar a outras salas
    G.add_edge('elevador_quarto_piso', 'auditorio_quarto_piso', weight=calcular_distancia(*posicoes['elevador_quarto_piso'], *posicoes['auditorio_quarto_piso']))

    # Conectar as outras salas entre si, conforme layout físico
    G.add_edge(4013, 4010, weight=calcular_distancia(*posicoes[4013], *posicoes[4010]))
    G.add_edge(4014, 4013, weight=calcular_distancia(*posicoes[4014], *posicoes[4013]))

    return G

# Função para buscar a sala no banco de dados e gerar o gráfico 3D
def buscar_sala(nome, modo_transporte):
    try:
        # Verifique se nome é uma string válida
        if not isinstance(nome, str) or not nome.strip():
            print("Erro: insira um nome válido.")
            return
        
        nome = nome.lower()  # Converte o nome para minúsculas
        
        # Conecte ao banco de dados e faça a pesquisa
        banco = sqlite3.connect('wazime.db')
        cursor = banco.cursor()
        cursor.execute("SELECT Nome, Secao, Sala FROM cadastro WHERE LOWER(Nome) = ?", (nome,))
        resultado = cursor.fetchone()

        if resultado:
            nome, secao, sala = resultado
            print(f"Nome: {nome}, Seção: {secao}, Sala: {sala}")
            sala_destino = sala
            
            # Construir o grafo com base no modo de transporte escolhido
            G = construir_grafo(modo_transporte)
            
            if sala_destino in G.nodes:
                start_node = 'guarda'  # Supondo que 'guarda' seja o ponto inicial
                # Calcula o caminho mais curto usando NetworkX
                try:
                    path = nx.shortest_path(G, start_node, int(sala_destino), weight='weight')
                    print(f"Caminho mais curto para {sala}: {' -> '.join(map(str, path))}")
                    
                    # Visualiza o grafo e o caminho mais curto
                    visualizar_caminho(path, G)
                except nx.NetworkXNoPath:
                    print(f"Não há caminho para a sala {sala_destino} no grafo.")
            else:
                print(f"Sala {sala} não está no grafo.")
        else:
            print(f"Nome {nome} não encontrado no banco de dados.")

        banco.close()

    except sqlite3.Error as erro:
        print("Erro ao realizar a pesquisa:", erro)

# Função para visualizar o caminho mais curto no gráfico 3D
def visualizar_caminho(path, G):
    pos = {
        'guarda': (2, 0, 0),                           # Primeiro andar (z=0)
        'escada_esquerda_primeiro_piso': (1.75, 0.75, 0),             
        'elevador_esquerdo_primeiro_piso': (1.8, 0.75, 0),
        'escada_esquerda_quarto_piso': (1.75, 0.75, 3),
        'elevador_quarto_piso': (1.8, 0.75, 3),
        4007: (1.25,0,3),
        4010: (1, 0, 3),
        4013: (0.5, 0, 3),
        4014: (0, 0, 3),
        'salao_de_honra': (2, 0, 3),
        'sala_dos_professores': (1.5, 0, 3),
        'auditorio_quarto_piso': (2, 1, 3)
    }

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Desenhar nós no gráfico 3D
    for node, (x, y, z) in pos.items():
        if node in G.nodes:
            ax.scatter(x, y, z, s=200, c='lightgreen', label=str(node), depthshade=True)
            ax.text(x, y, z, s=str(node), fontsize=12)

    # Desenhar o caminho mais curto no gráfico 3D
    for edge in zip(path, path[1:]):
        x_values = [pos[edge[0]][0], pos[edge[1]][0]]
        y_values = [pos[edge[0]][1], pos[edge[1]][1]]
        z_values = [pos[edge[0]][2], pos[edge[1]][2]]
        ax.plot(x_values, y_values, z_values, c='red')

    # Definir rótulos dos eixos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Andares (Z)')

    plt.title("Gráfico 3D do Prédio com 4 Andares")
    plt.show()

# Função para cadastrar as informações no banco de dados SQLite
def cadastrar():
    nome = formulario.lineEdit.text()
    secao = formulario.lineEdit_2.text()
    sala = formulario.lineEdit_3.text()

    if not nome.strip() or not secao.strip() or not sala.strip():
        print("Erro: todos os campos devem ser preenchidos.")
        return

    try:
        banco = sqlite3.connect('wazime.db')
        cursor = banco.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cadastro (
                Nome TEXT,
                Secao TEXT,
                Sala TEXT
            )
        """)
        cursor.execute("INSERT INTO cadastro (Nome, Secao, Sala) VALUES (?, ?, ?)", (nome, secao, sala))

        banco.commit()
        banco.close()

        print("Dados inseridos com sucesso!")

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados:", erro)

# Função para pesquisar a sala
def pesquisar():
    nome = formulario.lineEdit.text()  # Pegue o valor do campo de texto
    modo_transporte = formulario.comboBox.currentText()  # Obtenha a escolha do usuário: escada ou elevador
    if not nome:  # Verifica se o nome está vazio
        print("Por favor, insira um nome válido.")
        return
    buscar_sala(nome, modo_transporte)

# Configuração da interface PyQt5
app = QtWidgets.QApplication([])

# Carrega o arquivo de interface
formulario = uic.loadUi("formulario2.ui")

# Adicionar opções no comboBox (Escada ou Elevador)
formulario.comboBox.addItem("escada")
formulario.comboBox.addItem("elevador")

# Conecta o botão de pesquisa à função de pesquisa e cadastro
formulario.pushButton_2.clicked.connect(pesquisar)
formulario.pushButton.clicked.connect(cadastrar)  # Botão "Cadastrar"

formulario.show()
app.exec()
