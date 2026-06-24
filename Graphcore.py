# -*- coding: utf-8 -*-
"""
Programador Felipe de Jesús Martínez Alfaro

Progama realizado para la materia de Teoría de grafos.
"""
import matplotlib.pyplot as plt
import networkx as nx;
import random;

class Graf(nx.Graph): # sobre escribo mi clase grafo de graph
  """                       Sobre carga de metodos                                          """
  def __init__(self,pesos_aleatorios = True,incoming_graph_data=None, **attr):
    super().__init__(incoming_graph_data, **attr)
    self.pesos_aleatorios = pesos_aleatorios

  def add_edge(self,u_of_edge, v_of_edge, **attr):
    if self.pesos_aleatorios:
      attr['weight'] = random.randint(1,15)
    else:
      attr['weight'] = 1
    super().add_edge(u_of_edge, v_of_edge, **attr)

  """                     Funciones escenciales                                  """
  # Indica la cantidad de aristas que se pueden crear de acuerdo a un numero de nodos...
  def posibles(self):
    n = len(self) - 1 # Porque no se consideran los lazos.
    return (n**2 + n) // 2            # La cantidad de aristas posibles que pueden existir

  def getAristas(self,descendente = True):
    aristas = list(self.edges.data("weight", default=1))
    lista = []
    while aristas:
      lista.append(
          aristas.pop(
              aristas.index(
                  max(aristas, key=lambda x: x[2])
                  )
              )
          )
    return lista if descendente else lista[::-1];

  """                     Creación de grafos                                  """
  # Generar un grafo dada una suceción gráfica (s) que es un array ordenado de mayor a menor. O(m+n)
  def sucesion(self,s):
    # El array no está ordenado de mayor a menor?...
    if s != sorted(s,reverse=True):
      print("> La sucesión gráfica no es valida, ¡debe estar ordenada de mayor a menor!")
      return self;
    # Los grados de las aristas forman un numero par?...
    if sum(s)%2 != 0 :
      print("> La sucesión gráfica no es valida, ¡suma de grados impar!")
      return self;
    # Un nodo tiene un grado inexistente?...
    if max(s) >= len(s) or min(s) < 0:
      print("> La sucesión gráfica no es valida, ¡al menos un nodo tiene un grado imposible!")
      return self;
    if max(s) == 0:
      self.add_nodes_from(range(len(s)))
      return self;
    # Inicializo...
    nodos = len(s)
    self.add_nodes_from(range(nodos)) # Creo los nodos del grafo.
    count = s[0]
    u = 0 # Pibote.
    s.pop(0)
    v = 0 # A conectar.
    while( len(s) > 0 ):
      # No se puede conectar con v...
      if(s[v]==0):
        print("> La sucesión gráfica no es valida, ¡los grados son incoherentes!, ejemplo, [1,0].")
        return Graf();
      # Realiza una conexión...
      self.add_edge(u,u+1+v)
      count -= 1
      s[v] -= 1
      v += 1
      # Si u se ha acabado sus conexiones...
      if count == 0:
        while(count == 0 and len(s) > 0):
          count = s[0]
          s.pop(0)
          u += 1
          v = s.index(max(s)) if len(s) > 0 else 0
          if u >= nodos: break;
    return self;

  # Generar grafos r-regulares de orden n.
  def regular(self,r,n):
    if r>=n:
      print("> Valor no valido para r.")
      return self;
    return self.sucesion([r]*n);


  # gnm. Aristas al azar. Crea n nodos y elegir uniformemente al azar m distintos pares de distintos vértices.
  def erdosRenyi(self,nodos,aristas):
    self.add_nodes_from(range(nodos)) # Creo los nodos del grafo.
    # Para que no se pasen de lanza...
    if(self.posibles() < aristas  ):
      print("> No es posible crear tantas aristas con esos nodos en un grafo simple.")
      return self;
    # Verifico las posibilidades de crear las aristas con cada nodo aplicando producto cruz...
    mxn = []          # lista que maneja los prodctos cruz posibles (aristas posibles)
    for i in range(nodos):
      for j in range(i+1,nodos):
        mxn.append((i,j));            # {(m,n): m in V y n in V }
    # Empiezo a crear aristas...
    i = 0
    while(i < aristas):
      ari = random.choice(mxn)        # Selecciono una arista de los posibles.
      mxn.pop(mxn.index(ari))         # Elimino la posibilidad.
      self.add_edge(ari[0],ari[1])    # Agrego la arista al grafo.
      i += 1                          # Incremento el numero de aristas posibles.
    return self;

  # Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada par independiente y uniformemente con probabilidad p.
  def gilbert(self,nodos,probabilidad):
    if (probabilidad > 1 or probabilidad <= 0):
      if probabilidad != 0:
          print("> ERROR!! La probabilidad debe variar entre 0 y 1")
      return self;
    self.add_nodes_from(range(nodos)) # Creo los nodos del grafo.
    # Verifico las posibilidades de crear las aristas con cada nodo aplicando producto cruz...
    mxn = []          # lista que maneja los prodctos cruz posibles (aristas posibles)
    for i in range(nodos):
      for j in range(i+1,nodos):
        if random.random() < probabilidad:
          self.add_edge(i,j);         # Agrego la arista (i,j) si el evento pasa la probabilidad.
    return self;

  # Variante del modelo Gn,d Barabási-Albert. Colocar n nodos uno por uno, asignando a cada uno d aristas a vértices distintos
  # de tal manera que la probabilidad de que el vértice nuevo se conecte a un vértice existente v es proporcional a la cantidad de aristas que v tiene actualmente los primeros d vértices se conecta todos a todos.
  def barabasiAlbert(self,nodos,d_aristas):
    self.add_nodes_from(range(nodos),frec = 0)    # Creo los nodos del grafo. Con el parámetro de frecuencia acumlada.
    # Verificaciones...
    if d_aristas == 0 or d_aristas > len(self):
      print("> ¡Valor no valido para d!")
      return self;
    # Conectamos los nodos...
    for i in range(nodos):
      for j in range(i+1,nodos):      # Exploramos todas las posibilidades MxN
        if j <= d_aristas:            # las primeras d aristas se conectan en un grafo Kd (completo).
          self.add_edge(i,j);         # Añado la arista.
          self.nodes[i]['frec'] += 1  # Incremento la frecuencia acumulada de i.
          self.nodes[j]['frec'] += 1  # Incremento la frecuencia acumulada de j.
        elif random.random() <= self.nodes[i]['frec']/self.size():  # Las demás aristas se calculan según la p = frec/n
          self.add_edge(i,j);         # Añado la arista.
          self.nodes[i]['frec'] += 1  # Incremento la frecuencia acumulada de i.
          self.nodes[j]['frec'] += 1  # Incremento la frecuencia acumulada de j.
    return self;

    # Crea un grafo con Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo.
    # Después, para cada nodo adicional, se selecciona una arista al azar y se crean aristas entre
    # el nodo nuevo y los extremos de la arista seleccionada.
  def dorogovtsevMendes(self,nodos,pre = ''):
      if nodos < 3:
        print("> ¡Valor no valido para los nodos!")
        return self;
      self.add_nodes_from(range(3))   # Creo los nodos del grafo.
      # Realizo el triángulo...
      self.add_edge(0,1)
      self.add_edge(0,2)
      self.add_edge(1,2)
      # Conectamos los nodos...
      elegibles = list(self.edges)    # Que aristas puedo elegir.
      for i in range(3,nodos):
        ari = random.choice(elegibles)# Selecciono una arista al azar.
        elegibles.remove(ari)         # Elimino la posibilidad de que se elija.
        self.add_edge(i,ari[0])                   # Añado la arista (i,a).
        elegibles.append((i,ari[0]))  # Añado la posiblidad de ser elegida.
        self.add_edge(i,ari[1])                   # Añado la arista (i,b).
        elegibles.append((i,ari[1]))  # Añado la posiblidad de ser elegida.
      return self;

  """                     Operadores de grafos                                  """
  # Sobre escribo >> para indicar que la numeración de nodos de G continua a la de self.
  # Sea s in self y  g in G => s_0 != g_0 y g_0 = |self|
  def __rshift__(self,B):
    map = {}          # mapa que indidca el nuevo nombre de cada nodo de B.
    for i in range(len(B)):
      map[i] = len(self)+i            # El nuevo nombre será la continuación de la numeración de A.
    return nx.relabel_nodes(B,map);   # Renombro los nodos.

  # Sobrecargo '|' para representar la unión de A U B.
  def __or__(A,B):
    C = Graf()        # Grafo vacio.
    # V_A U V_B ...
    C.add_nodes_from(A)
    C.add_nodes_from(B)
    # E_A U E_B ...
    C.add_edges_from(A.edges)
    C.add_edges_from(B.edges)
    return C;

  # Sobre cargo '+' para representar la conccatenación A+B.
  # C = (V_{AUB},E_{AUB}U(V_AxV_B)).
  def __add__(A,B):
    # (V_{AUB},E_{AUB})...
    C = A|B
    # V_AxV_B ...
    AxB = []
    for a in list(A.nodes):
      for b in list(B.nodes):
        if a != b:    # Evitamos los lazos.
          AxB.append((a,b))
    # E_{AUB}U(V_AxV_B) ...
    C.add_edges_from(AxB)
    return C;

  # Sobrecargo '*' para representar el producto cruz AxB.
  # Sustituye el grafo A en cada nodo de B, y proyecta los subgrafos generados por A de acuerdo a las conexiones de B. (casi como B1 + B2).
  # AxB es isomorfo con BxA.
  def __mul__(A,B):
    C = Graf()
    # Calculo V_A x V_B...
    for a in list(A.nodes):
      for b in list(B.nodes):
        C.add_node((a,b));
    # Calculo E_{AxB}...
    nodos = list(C.nodes)
    for i in range(len(C)):
      for j in range(i+1,len(C)):
        u,x = nodos[i]
        v,y = nodos[j]
        # Realiza la proyección si hay relación...
        R_a = (u==v) and B.has_edge(x,y)
        R_b = (x==y) and A.has_edge(u,v)
        if R_a or R_b:
          C.add_edge(nodos[i],nodos[j])
    return C;

  """                                 Árboles                                   """
  # Prim, voy añadiendo nodos de acuerdo a las aristas de menor peso de los nodos anteriores.
  def prim(self):
    H = Graf()                        # Creo un nuevo grafo.
    # Obtengo las aristas de los nodos del primer nodo, así como los nodos del grafo...
    u = 0                             # Empiezo con el nodo 0.
    H.add_node(u)
    aristas = sorted(                 # Obtengo las aristas ordenadas que conectan con u.
        [ari for ari in list(self.edges.data("weight", default=1)) if ari[0] == u or ari[1] == u],
        #^Añado ari, para cada arista en la lista (las aristas de G con el dato de peso, si no tiene por default es 1), tal que se relacione con u.
        key = lambda n:n[2]
        )
    # Empiezo a añadir nodos y conectar con aristas de G...
    a = aristas.pop(0);               # Como es ascendente agarro la de menor peso.
    v = a[1]                          # v es el otro nodo.
    while aristas:                    # Mientras la lista no esté vacia.
      if not H.has_node(v):           # si v no ha sido agregado previamente.
        H.add_node(v)
        H.add_edge(u,v,weight = a[2])
        aristas = sorted( aristas +   # Actualizo la lista agregando las aristas salientes de v.
            [ari for ari in list(self.edges.data("weight", default=1)) if ari[0] == v or ari[1] == v],
            key = lambda n:n[2]
            )
      a = aristas.pop(0)              # tomo la siguiente arista de menor peso.
      u = a[0]
      v = a[1]
    return H;
  
  # Kruskal, voy añadiendo aristas de menor peso a mayor sin generar ciclos.
  def kruskal(self):
    H = Graf()                        # Creo otro grafo.
    H.add_nodes_from(self.nodes)      #Le añado todos los nodos de G.
    # Obtengo las arisats ordenadas de manera ascendente...
    aristas = self.getAristas(descendente = False)    # Obtengo las aristas de G en orden ascendente.
    # Comiensa algoritmo...
    while aristas:                    # Mientras la lista no esté vacia.
      a = aristas.pop()               # Obtengo la arista de menor peso (porque está en orden ascendente).
      if not nx.has_path(H,a[0],a[1]):# Si no hay un camino que conecte a u,v de a.
        H.add_edge(a[0],a[1],weight = a[2])
    return H;

  # Kruskal inverso.
  def IKruskal(self):
    """Advertencia: Esta función modifica el grafo original."""
    # Obtengo las arisats ordenadas de manera descendente...
    aristas = self.getAristas()       # Obtengo las aristas de G en orden descendente (mayor a menor).
    # Empiezo a desconectar aristas...
    while aristas:#count_a > self.number_of_nodes()-1: <- ya no por si es un grafo disconexo.
        a = aristas.pop()             # Tomo la arista más pesada.
        self.remove_edge(a[0],a[1])   # Primero el changlazo xD
        if not nx.has_path(self,a[0],a[1]):       # Desconeté el grafo???
          self.add_edge(a[0],a[1],weight = a[2])  # Upsss sorry te regreso.
    return self;
