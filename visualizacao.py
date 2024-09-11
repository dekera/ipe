import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import calcular_vetor_direcao, calcular_versor, produto_vetorial
from grafo import nome_formatado  # Importar o dicionário nome_formatado

# Função para gerar instruções de direção e andar
def gerar_instrucoes(caminho, posicoes):
    instrucoes = []
    
    for i in range(1, len(caminho) - 1):
        no_atual = caminho[i]
        no_anterior = caminho[i - 1]
        no_proximo = caminho[i + 1]
        
        # Coordenadas dos nós
        coord_anterior = posicoes[no_anterior]
        coord_atual = posicoes[no_atual]
        coord_proximo = posicoes[no_proximo]

        # Verificar se há mudança no andar (eixo z)
        if coord_anterior[2] != coord_atual[2]:
            if coord_atual[2] > coord_anterior[2]:
                instrucoes.append(f"Suba da {nome_formatado.get(no_anterior, no_anterior)} para a {nome_formatado.get(no_atual, no_atual)}.")
            else:
                instrucoes.append(f"Desça da {nome_formatado.get(no_anterior, no_anterior)} para a {nome_formatado.get(no_atual, no_atual)}.")
        else:
            # Calcular o vetor direção
            vetor_antes = calcular_vetor_direcao(coord_anterior, coord_atual)
            vetor_depois = calcular_vetor_direcao(coord_atual, coord_proximo)
            
            # Produto vetorial
            resultado = produto_vetorial(vetor_antes, vetor_depois)
            
            if resultado > 0:
                instrucoes.append(f"Vire à esquerda e siga até a {nome_formatado.get(no_atual, no_atual)}.")
            elif resultado < 0:
                instrucoes.append(f"Vire à direita e siga até a {nome_formatado.get(no_atual, no_atual)}.")
            else:
                instrucoes.append(f"Siga em frente até a {nome_formatado.get(no_atual, no_atual)}.")

    # Última instrução
    no_ultimo = caminho[-2]
    no_destino = caminho[-1]
    vetor_ultimo = calcular_vetor_direcao(posicoes[no_ultimo], posicoes[no_destino])
    vetor_penultimo = calcular_vetor_direcao(posicoes[caminho[-3]], posicoes[no_ultimo]) if len(caminho) > 2 else (1, 0)
    versor_anterior = calcular_versor(vetor_penultimo)
    resultado_final = produto_vetorial(versor_anterior, vetor_ultimo)

    if resultado_final > 0:
        instrucoes.append(f"Vire à esquerda e siga até a {nome_formatado.get(no_destino, no_destino)}.")
    elif resultado_final < 0:
        instrucoes.append(f"Vire à direita e siga até a {nome_formatado.get(no_destino, no_destino)}.")
    else:
        instrucoes.append(f"Siga em frente até a {nome_formatado.get(no_destino, no_destino)}.")

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
            ax.text(x + 0.08, y + 0.07, z + 0.05, s=str(nome_legivel), fontsize=10)

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