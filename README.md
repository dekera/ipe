# Projeto de Análise de Grafos e Banco de Dados

Este repositório contém um projeto que utiliza grafos para realizar análises de conectividade e distância, e faz uso de um banco de dados para armazenar informações.

## Estrutura do Projeto

- **`grafo.py`**: Contém a construção do grafo representando o edifício, conectando salas com base em modos de transporte (escada ou elevador) e calculando distâncias 3D entre elas.
- **`NETWORKX.py`**: Script principal que cria uma interface gráfica com PyQt5, permitindo a busca por salas no banco de dados e gerando o caminho mais curto com NetworkX.
- **`utils.py`**: Fornece funções auxiliares como o cálculo de distâncias euclidianas, vetores de direção, e produtos vetoriais.
- **`visualizacao.py`**: Utiliza Matplotlib para visualizar o grafo em 3D e gerar instruções de navegação para o usuário com base no caminho mais curto.
- **`formulario2.ui`**: Arquivo da interface gráfica criado com PyQt5 Designer, que gerencia a interação com o usuário.
- **`wazime.db`**: Banco de dados SQLite que armazena informações sobre as salas e seções do edifício.


## Funcionalidades

- **Construção de grafos**: Modelagem das conexões entre salas com base na escolha do modo de transporte (escada ou elevador).
- **Visualização 3D**: Exibição do grafo em um modelo tridimensional, destacando o caminho mais curto entre dois pontos.
- **Geração de instruções**: Geração de direções para o usuário, indicando quando virar, subir ou descer de andar.
- **Interface gráfica**: Permite busca e cadastro de informações de salas usando PyQt5 e banco de dados SQLite.

## Requisitos

- **Python 3.x**
- **Bibliotecas necessárias**:
  - `networkx`
  - `matplotlib`
  - `numpy`
  - `sqlite3`
  - `PyQt5`

Para instalar as bibliotecas necessárias, execute:

```bash
pip install networkx matplotlib numpy sqlite3 pyqt5
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
## Usando a Interface:
- Na interface, você pode cadastrar novas salas e seções no banco de dados.
- Pesquisar por uma sala já cadastrada e gerar instruções detalhadas de como chegar até ela.

## Organização do Código
- **Grafo e Cálculo de Distâncias:** O grafo é construído no arquivo grafo.py com base nas posições físicas das salas no edifício. A função calcular_distancia no arquivo utils.py é usada para calcular as distâncias entre as salas em 3D.

- **Visualização:** A função visualizar_e_instruir no arquivo visualizacao.py usa Matplotlib para mostrar o grafo em 3D e as instruções geradas para o caminho mais curto entre duas salas.

- **Banco de Dados:** As funções cadastrar e buscar_sala no arquivo NETWORKX.py lidam com o cadastro e a busca de salas no banco de dados wazime.db.

