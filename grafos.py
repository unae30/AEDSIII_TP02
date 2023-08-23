import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

class Grafos:
    
    def __init__(self):
        self.politicos = [] 
        self.partido = {}
        self.graph = nx.Graph()

    def ler_Politicians(self, politicians_file):
        try:
            with open("datas/politicians2002.txt", "r", encoding="utf-8") as politicians_file:
                politicos = politicians_file.read()  # Lê o conteúdo do arquivo para a variável politicos
                self.politicos = politicos.splitlines()  # Divide as linhas para preencher self.politicos

        except FileNotFoundError:
            print('Arquivo não encontrado!')
        except Exception as e:
            print('Erro ao abrir o arquivo:', e)

    def ler_Graph(self, graph_file):
        try:
            with open("datas/graph2002.txt", "r",encoding="utf-8") as graph_file:
                ligacao_politicos = graph_file.read()
                #print(ligacao_politicos)
        except FileNotFoundError:
            print('Arquivo não encontrado!')
        except Exception as e:
            print('Erro ao abrir o arquivo:', e)


    def criar_politico(self):

        partido_cores = {}  # Dicionário para mapear partidos a cores
        for i in range(len(self.politicos)):
            nome_completo, partido = self.politicos[i].split(';')[:2]
            nome = nome_completo.split()[0]
            self.graph.add_node(nome, partido=partido)
            if partido not in partido_cores:
                partido_cores[partido] = plt.cm.jet(len(partido_cores))  # Associe uma cor ao partido

        self.partido_cores = partido_cores  # Guarde o dicionário de cores no objeto
        #teste para saber se estão funcionando 
       #print(self.graph.nodes())
       #print(self.graph.nodes(data=True)) 

    def plotarGrafico(self):

        
        node_colors = [self.partido_cores[nodo["partido"]] for nodo in self.graph.nodes.values()]
        
        nx.draw(
            self.graph,
            with_labels=True,
            font_weight='bold',
            node_color=node_colors  # Defina as cores dos nós
        )
        plt.show()


    #necessário criar subgrafos para ver os nós dos partidos que queremos 
    def plotarPartido(self, partido):
        nodes_of_partido = [node for node, data in self.graph.nodes(data=True) if data.get("partido") == partido]
        subgraph = self.graph.subgraph(nodes_of_partido)
        
        node_colors = [self.partido_cores[nodo["partido"]] for nodo in subgraph.nodes.values()]
        
        nx.draw(
            subgraph,
            with_labels=True,
            font_weight='bold',
            node_color=node_colors
        )
        plt.show()



politicians_graph = Grafos()


#Trabalhando com os Políticos
politicians_graph.ler_Politicians('politicians2002.txt')
# Testando a função criar_politico()
politicians_graph.criar_politico()
# Plotar o grafo de políticos (exemplo)
#politicians_graph.plotarGrafico()
#plotar partido especifico"
politicians_graph.plotarPartido("PMDB")




#politicians_graph.ler_Graph('politicians2002.txt')


