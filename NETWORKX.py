import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sqlite3
from PyQt5 import uic, QtWidgets

# Função para construir o grafo com base na escolha do usuário (escada ou elevador)
def construir_grafo(modo_transporte):
    G = nx.Graph()

    # Adicionar nós
    G.add_node('guarda', floor=1)
    G.add_node('escada', floor=1)
    G.add_node('elevador1e', floor=1)
    G.add_node(4010, floor=4)  # Quarto andar
    
    # Remover qualquer conexão desnecessária dependendo da escolha do usuário
    if modo_transporte == 'escada':
        # Se a escolha for escada, não conecte ao elevador
        G.add_edge('guarda', 'escada', weight=2)
        G.add_edge('escada', 4010, weight=9)  # Somente rota pela escada
    elif modo_transporte == 'elevador':
        # Se a escolha for elevador, não conecte à escada
        G.add_edge('guarda', 'elevador1e', weight=1)
        G.add_edge('elevador1e', 4010, weight=10)  # Somente rota pelo elevador

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
        'guarda': (0, 0, 0),        # Primeiro andar (z=0)
        'escada': (1, 0, 0),        # Primeiro andar (z=0)
        'elevador1e': (2, 0, 0),    # Primeiro andar (z=0)
        4010: (1, 0, 3)             # Quarto andar (z=3)
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
    nome = formulario2.lineEdit.text()
    secao = formulario2.lineEdit_2.text()
    sala = formulario2.lineEdit_3.text()

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
    nome = formulario2.lineEdit.text()  # Pegue o valor do campo de texto
    modo_transporte = formulario2.comboBox.currentText()  # Obtenha a escolha do usuário: escada ou elevador
    if not nome:  # Verifica se o nome está vazio
        print("Por favor, insira um nome válido.")
        return
    buscar_sala(nome, modo_transporte)

# Configuração da interface PyQt5
app = QtWidgets.QApplication([])

# Carrega o arquivo de interface
formulario2 = uic.loadUi("formulario2.ui")

# Adicionar opções no comboBox (Escada ou Elevador)
formulario2.comboBox.addItem("escada")
formulario2.comboBox.addItem("elevador")

# Conecta o botão de pesquisa à função de pesquisa e cadastro
formulario2.pushButton_2.clicked.connect(pesquisar)
formulario2.pushButton.clicked.connect(cadastrar)  # Botão "Cadastrar"

formulario2.show()
app.exec()
