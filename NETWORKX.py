import sqlite3
from PyQt5 import uic, QtWidgets
from grafo import construir_grafo
from visualizacao import visualizar_e_instruir
import networkx as nx

# Função para buscar a sala no banco de dados e gerar o gráfico 3D
def buscar_sala(nome, modo_transporte):
    try:
        if not isinstance(nome, str) or not nome.strip():
            print("Erro: insira um nome válido.")
            return
        
        nome = nome.lower()
        banco = sqlite3.connect('wazime.db')
        cursor = banco.cursor()
        cursor.execute("SELECT Nome, Secao, Sala FROM cadastro WHERE LOWER(Nome) = ?", (nome,))
        resultado = cursor.fetchone()

        if resultado:
            nome, secao, sala = resultado
            sala_destino = int(sala)
            G, pos = construir_grafo(modo_transporte)
            if sala_destino in G.nodes:
                path = nx.shortest_path(G, 'guarda', sala_destino, weight='weight')
                visualizar_e_instruir(path, G, pos)  # Não precisa mais passar `nome_formatado`
            else:
                print(f"Sala {sala_destino} não está no grafo.")
        else:
            print(f"Nome {nome} não encontrado no banco de dados.")
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
