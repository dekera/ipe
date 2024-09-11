# Projeto de Análise de Grafos e Banco de Dados

Este repositório contém um projeto que utiliza grafos para realizar análises de conectividade e distância, e faz uso de um banco de dados para armazenar informações.

## Estrutura do Projeto

- **`NETWORKX.py`**: Este é o arquivo principal e contém a implementação das funções para a criação, manipulação e análise dos grafos utilizando a biblioteca `NetworkX`.
- **`controlepesquisaedistancia.py`**: (Não usa o NETWORKX) Script responsável por controlar as pesquisas de caminhos e distâncias no grafo, além de funções auxiliares para otimização.
- **`formulario.ui`** e **`formulario2.ui`**: Interfaces gráficas desenvolvidas utilizando o framework PyQt para interação com o usuário.
- **`wazime.db`**: Banco de dados SQLite contendo as informações que alimentam o sistema de grafos que são: nome, sala e seção.

## Funcionalidades

- Criação e manipulação de grafos utilizando `NetworkX`.
- Pesquisa de menores caminhos e distâncias em grafos.
- Interface gráfica para facilitar a interação com os dados e os resultados das pesquisas.
- Integração com banco de dados SQLite para armazenamento de dados de nós e arestas.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `networkx`
  - `sqlite3`
  - `PyQt5`

Para instalar as bibliotecas necessárias, execute:

```bash
pip install networkx sqlite3 pyqt5
```
## Como Utilizar

- Clone o repositório:
```bash
https://github.com/dekera/ipe.git
```
- Navegue até a pasta do projeto:
```bash
cd ipe
```
- Navegue até a pasta do projeto:
```bash
python NETWORKX.py
```
