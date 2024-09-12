import sqlite3
from PyQt5 import uic, QtWidgets
from grafo import construir_grafo
from visualizacao1 import visualizar_e_instruir
import networkx as nx


# Função para buscar a sala no banco de dados e gerar o gráfico 3D
def buscar_sala(nome_ou_sala, modo_transporte):
    try:
        banco = sqlite3.connect('wazime.db')
        cursor = banco.cursor()
        
        # Se a entrada for um número, assume-se que é uma sala numérica
        if nome_ou_sala.isdigit():  # Se a entrada for um número
            sala_destino = nome_ou_sala
            cursor.execute("SELECT Nome, Secao, Sala FROM cadastro WHERE Sala = ?", (sala_destino,))
            resultado = cursor.fetchone()
        
        else:  # Se não for número, trata-se de um nome ou nome de sala como 'biblioteca'
            nome = nome_ou_sala.lower()
            cursor.execute("SELECT Nome, Secao, Sala FROM cadastro WHERE LOWER(Nome) = ? OR LOWER(Sala) = ?", (nome, nome))
            resultado = cursor.fetchone()

        if resultado:
            nome, secao, sala = resultado
            print(f"Nome: {nome}, Seção: {secao}, Sala: {sala}")

            # Verifica se a sala é uma string ou número
            if isinstance(sala, int) or str(sala).isdigit():  # Tratar como número se for inteiro ou string numérica
                sala_destino = int(sala)
            else:
                sala_destino = sala  # Se for string, como "biblioteca"

            # Construir o grafo com base no modo de transporte escolhido
            G, pos = construir_grafo(modo_transporte)

            if sala_destino in G.nodes:
                path = nx.shortest_path(G, 'guarda', sala_destino, weight='weight')
                visualizar_e_instruir(path, G, pos)
            else:
                print(f"Sala {sala_destino} não está no grafo.")
        else:
            print(f"Nome ou sala {nome_ou_sala} não foi encontrado no banco de dados.")

        banco.close()

    except sqlite3.Error as erro:
        print("Erro ao realizar a pesquisa:", erro)


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
        cursor.execute("""CREATE TABLE IF NOT EXISTS cadastro (Nome TEXT, Secao TEXT, Sala TEXT)""")
        cursor.execute("INSERT INTO cadastro (Nome, Secao, Sala) VALUES (?, ?, ?)", (nome, secao, sala))
        banco.commit()
        banco.close()
        print("Dados inseridos com sucesso!")
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados:", erro)

# Função para pesquisar a sala
def pesquisar():
    nome = formulario.lineEdit.text()
    modo_transporte = formulario.comboBox.currentText()
    if not nome:
        print("Por favor, insira um nome válido.")
        return
    buscar_sala(nome, modo_transporte)

# Configuração da interface PyQt5
app = QtWidgets.QApplication([])

formulario = uic.loadUi("formulario2.ui")
formulario.comboBox.addItem("escada")
formulario.comboBox.addItem("elevador")

formulario.pushButton_2.clicked.connect(pesquisar)
formulario.pushButton.clicked.connect(cadastrar)

formulario.show()
app.exec()