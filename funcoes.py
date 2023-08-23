import os
import grafoPonderado as gp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import re
import random
import scipy as sp
import sys

def funcoes_grafos(AnoFiltrado, threshold, PartidoFiltrado):
    if PartidoFiltrado != '':
        PartidoFiltrado = PartidoFiltrado.replace(" ", "")
        PartidoFiltrado = PartidoFiltrado.split(",")

    # encotrar o endereço dos arquivos
    arq_graph = os.path.join("banco_de_dados", f"graph{AnoFiltrado}.txt")
    arq_politicians = os.path.join("banco_de_dados", f"politicians{AnoFiltrado}.txt")

    #ler os arquivos
    if os.path.exists(arq_graph):
        with open(arq_graph, "r", encoding="utf-8", errors="replace") as arquivo:
            conteudo_graph = arquivo.read()
        
    else:
        print("O arquivo não foi encontrado.")
        sys.exit()

    if os.path.exists(arq_politicians):
        with open(arq_politicians, "r", encoding="utf-8", errors="replace") as arquivo:
            conteudo_politicians = arquivo.read()
    else:
        print("O arquivo não foi encontrado.")
        sys.exit()

    print("Sucesso ao ler os arquivos. \nProcessando...")

    # Filtro dos partidos
    deputados = []
    for linha in conteudo_politicians.split("\n"):
        partes = linha.strip().split(";")
        if PartidoFiltrado != '':
            if len(partes) >= 2 and partes[1] in PartidoFiltrado:
                deputados.append(partes[0])
        else:
            if len(partes) >= 2:
                deputados.append(partes[0])

    #Arestas (votos em comum)
    votacoes = []
    for linha in conteudo_graph.split("\n"):
        partes = linha.strip().split(";")
        if len(partes) >= 2 and partes[0] in deputados and partes[1] in deputados:
            votacoes.append(linha)

    #Normalização
    votosDosDeputados = {}
    for linha in conteudo_politicians.split("\n"):
        partes = linha.strip().split(";")
        if len(partes) >= 2 and partes[0] in deputados:
            votosDosDeputados[partes[0]] = {'total': partes[2], 'partido': partes[1]}

    VNormalizadas = []
    for votos in votacoes:
        partes = votos.strip().split(";")
        vlr1 = votosDosDeputados[partes[0]]['total']
        vlr2 = votosDosDeputados[partes[1]]['total']
        pesoNv = int(partes[2]) / min(int(vlr1), int(vlr2))
        votos = "(" + votosDosDeputados[partes[0]]['partido'] + ") " + partes[0] + ";" +  "(" + votosDosDeputados[partes[1]]['partido'] + ") " + partes[1] + ";" + str(pesoNv)
        VNormalizadas.append(votos)
    votosNormalizados = sorted(VNormalizadas)

    #muda O o formato dos deputados
    deptd_2 = []
    for linha in conteudo_politicians.split("\n"):
        partes = linha.strip().split(";")
        if PartidoFiltrado != '':
            if len(partes) >= 2 and partes[1] in PartidoFiltrado:
                deptd_2.append("(" + partes[1] + ") " + partes[0])
        else:
            if len(partes) >= 2:
                deptd_2.append("(" + partes[1] + ") " + partes[0])

    deputados_2 = sorted(deptd_2)

    grafoNormalizado = gp.GrafoPonderado()
    grafoNormalizado.adiciona_nos(deputados_2)

    for l in votosNormalizados:
        partes = l.strip().split(";")
        grafoNormalizado.adicionar_aresta(partes[0], partes[1], partes[2])

    #threshold
    votacoesThreshold = []
    for votos in votosNormalizados:
        partes = votos.strip().split(";")
        if float(partes[2]) >= float(threshold):
            votacoesThreshold.append(votos)

    #Pesos invertidos 
    votacoesInversao = []
    for votos in votacoesThreshold:
        partes = votos.strip().split(";")
        pesoNv = 1 - float(partes[2])
        votos = partes[0] + ";" + partes[1] + ";" + str(pesoNv)
        votacoesInversao.append(votos)

    #grafo threshold
    grafo = gp.GrafoPonderado()
    grafo.adiciona_nos(deputados_2) 
    for linha in votacoesInversao:
        partes = linha.strip().split(";")
        grafo.adicionar_aresta(partes[0], partes[1], partes[2])

    #Centralidade
    G = nx.Graph()
    for node in grafo.lista_adj:
        G.add_node(node)

    for node, neighbors in grafo.lista_adj.items():
        for neighbor, weight_str in neighbors.items():
            weight = float(weight_str)
            G.add_edge(node, neighbor, weight=weight)

    centralidade = nx.betweenness_centrality(G)
    #Centralidade ordenada
    centralidade = {k: v for k, v in sorted(centralidade.items(), key=lambda item: item[1], reverse=True)}

    #Grafo plotado
    plt.figure(figsize=(10, 10))

    if PartidoFiltrado != '':
        plt.title(f"Votos dos deputados do {PartidoFiltrado} - ano {AnoFiltrado}")
    else:
        plt.title(f"Votos dos deputados - ano {AnoFiltrado}")
    plt.bar(centralidade.keys(), centralidade.values(), color='b')
    plt.xlabel("Deputados")
    plt.ylabel("Centralidade de intermediação")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    if PartidoFiltrado != '':
        plt.savefig(f"betwenness{AnoFiltrado}{PartidoFiltrado}.png")
    else:
        plt.savefig(f"betwenness{AnoFiltrado}.png")
    plt.close()

    # #heatmap
    nodes = list(grafoNormalizado.lista_adj.keys())
    node_indices = {node: i for i, node in enumerate(nodes)}
    num_nodes = len(nodes)
    heatmap_data = np.zeros((num_nodes, num_nodes))
    for source_node, connections in grafoNormalizado.lista_adj.items():
        for target_node, value in connections.items():
            source_idx = node_indices[source_node]
            target_idx = node_indices[target_node]
            heatmap_data[source_idx][target_idx] = value

    plt.figure(figsize=(8, 6))
    if PartidoFiltrado != '':
        plt.title(f"Votos dos deputados do {PartidoFiltrado} - ano {AnoFiltrado}")
    else:
        plt.title(f"Votos dos deputados no ano de {AnoFiltrado}")
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    plt.xticks(np.arange(num_nodes), nodes, rotation=90, fontsize=4)
    plt.yticks(np.arange(num_nodes), nodes, fontsize=4)

    plt.colorbar()
    plt.tight_layout()
    if PartidoFiltrado != '':
        plt.savefig(f"heatmap{AnoFiltrado}{PartidoFiltrado}.png")
    else:
        plt.savefig(f"heatmap{AnoFiltrado}.png")
    plt.close()

    #Todos os partidos 
    partidos = []
    for linha in conteudo_politicians.split("\n"):
        partes = linha.strip().split(";")
        if len(partes) >= 2 and partes[1] not in partidos:
            partidos.append(partes[1])

    #gerando cores aleatorias para os partidos
    cores_partido = {partido: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for partido in partidos}

    def extrair_partido(node_name):
        match = re.search(r'\((.*?)\)', node_name)
        if match:
            return match.group(1)
        return None

    pos = nx.spring_layout(G)
    node_colors = [cores_partido[extrair_partido(node)] for node in G.nodes()]
    plt.figure(figsize=(15, 20))
    nx.draw(G, pos=pos, with_labels=True, node_size=80, node_color=node_colors, font_size=8, font_color='black', font_weight='bold', width=0.5, edge_color='black')
    legend_labels = []
    for partido, color in cores_partido.items():
        if any(extrair_partido(node) == partido for node in G.nodes()):
            legend_labels.append(plt.Line2D([0], [0], color=color, lw=6, label=partido))
    plt.legend(handles=legend_labels, loc='upper right', fontsize=10)
    if PartidoFiltrado != '':
        plt.title(f"Grafo - Deputados do {PartidoFiltrado}, ano - {AnoFiltrado}")
    else:
        plt.title(f"Grafo - Deputados do {PartidoFiltrado}")
    if PartidoFiltrado != '':
        plt.savefig(f"graph{AnoFiltrado}{PartidoFiltrado}.png")
    else:
        plt.savefig(f"graph{AnoFiltrado}.png")
    plt.close()

    print ("Os plots foram salvos nos arquivos")
    if PartidoFiltrado != '':
        print(f"betwenness{AnoFiltrado}{PartidoFiltrado}.png")
        print(f"heatmap{AnoFiltrado}{PartidoFiltrado}.png")
        print(f"graph {AnoFiltrado}{PartidoFiltrado}.png")
    else:
        print(f"betwenness{AnoFiltrado}.png")
        print(f"heatmap{AnoFiltrado}.png")
        print(f"graph{AnoFiltrado}.png")