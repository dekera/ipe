import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import calcular_vetor_direcao, calcular_versor, produto_vetorial
from grafo import nome_formatado  # Importar o dicionário nome_formatado
import numpy as np

# Função para gerar instruções de direção e de andar com base no caminho
def gerar_instrucoes(caminho, posicoes):
    instrucoes = []
    
    # Inicializar o versor caminhado com um vetor neutro
    versor_caminhado = (1, 0)  # Inicialmente assume que o caminho é na direção do eixo x positivo

    for i in range(1, len(caminho)):
        no_atual = caminho[i]
        no_anterior = caminho[i - 1]
        
        # Se não for o último nó, calcular o próximo nó
        if i < len(caminho) - 1:
            no_proximo = caminho[i + 1]
        else:
            no_proximo = None  # Não há próximo nó no último ciclo
        
        # Coordenadas dos nós
        coord_anterior = posicoes[no_anterior]
        coord_atual = posicoes[no_atual]
        
        if no_proximo is not None:
            coord_proximo = posicoes[no_proximo]
        
        # Verificar se há mudança no andar (eixo z)
        if coord_anterior[2] != coord_atual[2]:
            if coord_atual[2] > coord_anterior[2]:
                instrucoes.append(f"Suba {nome_formatado.get(no_anterior, no_anterior)} para {nome_formatado.get(no_atual, no_atual)}.")
            else:
                instrucoes.append(f"Desça {nome_formatado.get(no_anterior, no_anterior)} para {nome_formatado.get(no_atual, no_atual)}.")
        else:
            # Calcular o versor caminhado (do nó anterior até o nó atual)
            vetor_caminhado = calcular_vetor_direcao(coord_anterior, coord_atual)
            versor_caminhado = calcular_versor(vetor_caminhado)
            
            if no_proximo is not None:
                # Calcular o versor seguinte (do nó atual até o nó proximo)
                vetor_seguinte = calcular_vetor_direcao(coord_atual, coord_proximo)
                versor_seguinte = calcular_versor(vetor_seguinte)

                # Calcular o produto vetorial entre o versor caminhado e o versor seguinte
                resultado = produto_vetorial(versor_caminhado, versor_seguinte)
                
                if np.isclose(resultado, 0, atol=0.02):
                    instrucoes.append(f"Siga em frente até {nome_formatado.get(no_atual, no_atual)}.")
                elif resultado > 0:
                    instrucoes.append(f"Siga até {nome_formatado.get(no_atual, no_atual)} e vire à esquerda.")
                elif resultado < 0:
                    instrucoes.append(f"Siga até {nome_formatado.get(no_atual, no_atual)} e vire à direita.")
            else:
                # No caso do último nó, não há próximo nó, portanto, apenas siga em frente até o destino final
                instrucoes.append(f"Siga em frente até {nome_formatado.get(no_atual, no_atual)}.")

        # Atualizar o versor caminhado para o próximo ciclo
        versor_caminhado = calcular_versor(calcular_vetor_direcao(coord_anterior, coord_atual))

    return instrucoes

# Função para visualizar o grafo 3D e as instruções
def visualizar_e_instruir(path, G, pos):
    # Aumentar o tamanho da figura
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Ajustar os limites dos eixos para melhorar a visualização
    ax.set_xlim([0, 3])  # Limite do eixo X
    ax.set_ylim([0, 1.5])  # Limite do eixo Y
    ax.set_zlim([0, 3.5])  # Limite do eixo Z (andares)

    # Desenhar nós no gráfico 3D
    for node, (x, y, z) in pos.items():
        if node in G.nodes:
            # Usar o nome formatado ou o nome original se não houver formatação
            nome_legivel = nome_formatado.get(node, node)
            ax.scatter(x, y, z, s=200, c='lightgreen', label=str(nome_legivel), depthshade=True)
            # Deslocar o texto para evitar sobreposição
            ax.text(x + 0.05, y, z + 0.05, s=str(nome_legivel), fontsize=10)

    # Desenhar o caminho mais curto no gráfico 3D
    for edge in zip(path, path[1:]):
        x_values = [pos[edge[0]][0], pos[edge[1]][0]]
        y_values = [pos[edge[0]][1], pos[edge[1]][1]]
        z_values = [pos[edge[0]][2], pos[edge[1]][2]]
        ax.plot(x_values, y_values, z_values, c='red')

    # Gerar e exibir instruções
    instrucoes = gerar_instrucoes(path, pos)
    
    for instrucao in instrucoes:
        print(instrucao)

    # Definir rótulos dos eixos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Andares (Z)')
    plt.title("Gráfico 3D do Prédio com 4 Andares")
    plt.show()