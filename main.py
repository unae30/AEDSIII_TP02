import funcoes as f

print("\n----Análise de deputados, partidos e votações----\n")
AnoFiltrado = input("Informe o ano a considerar (de 2001 a 2023): ")
threshold = input("Informe o percentual mínimo de concordância ( threshold ) (ex. 0.9): ")
PartidoFiltrado = input("Informe os partidos a analisar , separados por virgulas (ex. PT,MDB,PL): ")

if __name__ == "__main__":
    f.funcoes_grafos(AnoFiltrado, threshold, PartidoFiltrado)




