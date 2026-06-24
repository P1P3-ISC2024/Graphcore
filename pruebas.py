from Graphcore import Graf;
import networkx as nx;

# Para un grafo pequeño usamos una secuencia inventada...
G = Graf().sucesion( [3,3,3,2,1] )
nx.write_gexf(G,"5_sucesion.gexf")  # GEXF es ideal para Gephi.
# Probamos los árboles que se generan con Prim, Kruskal y Kruskal invertido...
G1 = G.prim()
G2 = G.kruskal()
G.IKruskal()
nx.write_gexf(G1,"5_sucesion_prim.gexf")
nx.write_gexf(G2,"5_sucesion_kruskal.gexf")
nx.write_gexf(G,"5_sucesion_kruskalInverso.gexf")



# Para un grafo mediano usamos un grafo 4 regular de orden 50...
G = Graf().regular(4,50)
nx.write_gexf(G,"50_4regular.gexf")
# Probamos los árboles que se generan con Prim, Kruskal y Kruskal invertido...
G1 = G.prim()
G2 = G.kruskal()
G3 = G.IKruskal()
nx.write_gexf(G1,"50_4regular_prim.gexf")
nx.write_gexf(G2,"50_4regular_kruskal.gexf")
nx.write_gexf(G,"50_4regular_kruskalInverso.gexf")




# Para un grafo grande usamos Dorogovtsev Mendes con 500 nodos...
H = Graf().dorogovtsevMendes(500)
# Luego paso sus nodos a una secuencia de grados...
s = sorted( [H.degree[n] for n in H.nodes] , reverse=True)
# Ahora sí recreo el grafo con esa secuencia...
G = Graf().sucesion(s)
nx.write_gexf(G,"500_DorogovtsevMendes_sucesion.gexf")
# Probamos los árboles que se generan con Prim, Kruskal y Kruskal invertido...
G1 = G.prim()
G2 = G.kruskal()
G3 = G.IKruskal()
nx.write_gexf(G1,"500_DorogovtsevMendes_sucesion_prim.gexf")
nx.write_gexf(G2,"500_DorogovtsevMendes_sucesion_kruskal.gexf")
nx.write_gexf(G,"500_DorogovtsevMendes_sucesion_kruskalInverso.gexf")
