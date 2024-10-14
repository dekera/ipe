import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from utils import calcular_vetor_direcao, calcular_versor, produto_vetorial
from grafo import nome_formatado
import numpy as np

# Função para gerar instruções de direção e de andar com base no caminho
def gerar_instrucoes(caminho, posicoes):
    instrucoes = []

    for i in range(1, len(caminho)):
        no_atual = caminho[i]
        no_anterior = caminho[i - 1]
        
        # Coordenadas dos nós
        coord_anterior = posicoes[no_anterior]
        coord_atual = posicoes[no_atual]

        # Verificar se há mudança de andar (eixo Z)
        if coord_anterior[2] != coord_atual[2]:
            if coord_atual[2] > coord_anterior[2]:
                instrucoes.append(f"Suba de {nome_formatado.get(no_anterior, no_anterior)} para o {nome_formatado.get(no_atual, no_atual)}.")
            else:
                instrucoes.append(f"Desça de {nome_formatado.get(no_anterior, no_anterior)} para o {nome_formatado.get(no_atual, no_atual)}.")
        else:
            # Se estiver no mesmo andar, calcular direção
            vetor_caminhado = calcular_vetor_direcao(coord_anterior, coord_atual)
            versor_atual = calcular_versor(vetor_caminhado)

            if i < len(caminho) - 1:
                no_proximo = caminho[i + 1]
                coord_proximo = posicoes[no_proximo]
                vetor_seguinte = calcular_vetor_direcao(coord_atual, coord_proximo)
                versor_seguinte = calcular_versor(vetor_seguinte)

                resultado = produto_vetorial(versor_atual, versor_seguinte)
                
                if np.isclose(resultado, 0, atol=0.02):
                    instrucoes.append(f"Siga em frente até {nome_formatado.get(no_atual, no_atual)}.")
                elif resultado < 0:
                    instrucoes.append(f"Siga até {nome_formatado.get(no_atual, no_atual)} e vire à esquerda.")
                elif resultado > 0:
                    instrucoes.append(f"Siga até {nome_formatado.get(no_atual, no_atual)} e vire à direita.")
            else:
                # Último nó
                instrucoes.append(f"Siga em frente até {nome_formatado.get(no_atual, no_atual)}.")

    return instrucoes

def visualizar_e_instruir(path, pos, andar_imgs):
    instrucoes = gerar_instrucoes(path, pos)

    # Criar uma lista de andares distintos pelos quais o caminho passa
    andares_no_caminho = sorted(set(pos[no][2] for no in path))

    # Configurar a grade dos subplots (2 colunas, número de linhas depende da quantidade de andares)
    fig, axs = plt.subplots(nrows=len(andares_no_caminho) // 2 + len(andares_no_caminho) % 2, ncols=2, figsize=(12, 6))
    axs = axs.flatten()  # Garantir que temos um array 1D de subplots

    # Iterar sobre os andares presentes no caminho e plotar em cada subplot
    for idx, andar in enumerate(andares_no_caminho):
        caminho_no_andar = [no for no in path if pos[no][2] == andar]

        if andar in andar_imgs and len(caminho_no_andar) >= 1:
            visualizar_caminho_2d(caminho_no_andar, pos, andar, andar_imgs[andar], axs[idx])
        else:
            print(f"Sem caminho suficiente para visualização no andar {andar + 1} ou imagem não encontrada.")

    # Exibir as instruções
    for instrucao in instrucoes:
        print(instrucao)

    plt.tight_layout()
    plt.show()


# Função para visualizar o caminho em 2D em um subplot específico
def visualizar_caminho_2d(caminho, posicoes, andar, imagem_planta, ax):
    """
    Visualiza o caminho realizado em um andar específico sobre a planta do andar, dentro de um subplot.
    
    Parâmetros:
    - caminho: lista de nós (locais) no caminho deste andar.
    - posicoes: dicionário com coordenadas (x, y, z) de cada nó.
    - andar: número do andar em que o caminho está sendo traçado.
    - imagem_planta: caminho para a imagem da planta do andar correspondente.
    - ax: Subplot onde o gráfico será desenhado.
    """
    
    # Carregar a imagem da planta do andar
    img = mpimg.imread(imagem_planta)

    if len(caminho) == 1:
        print(f"Visualizando nó único no andar {andar + 1}.")
    
    # Coordenadas (x, y) no andar atual
    coords_x = [posicoes[no][0] for no in caminho]
    coords_y = [posicoes[no][1] for no in caminho]

    # Exibir a imagem do andar no subplot específico
    ax.imshow(img, extent=[0, img.shape[1], img.shape[0], 0])
    
    # Traçar o caminho (ou apenas o ponto se houver apenas um nó)
    ax.plot(coords_x, coords_y, marker='o', color='red', markersize=5, linewidth=2)
    ax.set_title(f'Caminho no Andar {andar + 1}')
    ax.axis('off')  # Remover os eixos para melhorar a visualização
