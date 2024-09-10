import heapq
from PyQt5 import uic, QtWidgets
import sqlite3

# Define o grafo com os caminhos entre as salas
graph = {
    'guarda': {'elevador1e': 1, 'escada': 2},
    'elevador1e': {4010: 10, 'guarda': 1},
    'escada': {4010: 9, 'guarda': 2},
    4010: {'escada': 10, 'elevador1e': 10}
} 

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    shortest_path = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, shortest_path

def buscar_sala(nome):
    try:
        banco = sqlite3.connect('wazime.db')
        cursor = banco.cursor()
        nome = nome.lower() 
        cursor.execute("SELECT Nome, Secao, Sala FROM cadastro WHERE LOWER(Nome) = ?", (nome,))
        resultado = cursor.fetchone()

        if resultado:
            nome, secao, sala = resultado
            print(f"Nome: {nome}, Seção: {secao}, Sala: {sala}")
            sala_destino = sala
            
            if sala_destino in graph:
                start_node = 'guarda'  # Supondo que 'Guarda' seja o ponto inicial
                distances, shortest_path = dijkstra(graph, start_node)

                path = []
                current = sala_destino
                while current != start_node:
                    path.append(current)
                    current = shortest_path.get(current)
                path.append(start_node)
                path.reverse()

                print(f"Caminho mais curto para {sala}: {' -> '.join(map(str, path))}")
            else:
                print(f"Sala {sala} não está no grafo.")
        else:
            print(f"Nome {nome} não encontrado no banco de dados.")

        banco.close()

    except sqlite3.Error as erro:
        print("Erro ao realizar a pesquisa:", erro)

def pesquisar():
    nome = formulario.lineEdit.text()
    buscar_sala(nome)

# Função para cadastrar as informações no banco de dados SQLite.
def cadastrar():
    nome = formulario.lineEdit.text()
    secao = formulario.lineEdit_2.text()
    sala = formulario.lineEdit_3.text()

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

# Certifique-se de criar o QApplication antes de criar o widget
app = QtWidgets.QApplication([])

# Carrega o arquivo de interface
formulario = uic.loadUi("formulario.ui")

# Conecta o botão de pesquisa à função de pesquisa e cadastro
formulario.pushButton_2.clicked.connect(pesquisar)
formulario.pushButton.clicked.connect(cadastrar)  # Botão "Cadastrar"

formulario.show()
app.exec()
