from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapA={}

    def creaGrafo(self,anno,stato):
        self._graph.clear()
        nodi = DAO.getNodi(anno,stato)
        for n in nodi:
            self._idMapA[n.id] = n
            self._graph.add_node(n)

        archi = DAO.getArchi(anno, stato, self._idMapA)
        for a in archi:
            if a.a1.distance_HV(a.a2)<=100:
                self._graph.add_edge(a.a1, a.a2)

    def getCompConnesse(self):
            return nx.number_connected_components(self._graph)

    def compConnMaggiore(self):
        componenti = list(nx.connected_components(self._graph))
        if len(componenti) == 0:
            return 0
        componente_max = max(componenti, key=len)
        listaComponenti = list(componente_max)
        return (listaComponenti, len(componente_max))

    def getAnni(self):
        return DAO.getAnni()

    def getForma(self):
        return DAO.getForme()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
