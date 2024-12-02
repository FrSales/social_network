import matplotlib.pyplot as plt
import networkx as nx
import mplcursors  

class Grafo:
    def __init__(self):
        self.grafo = {}  
        self.vertices = set()  
        self.interesses = {}  

    def adicionar_aresta(self, v: str, w: str):
        if v not in self.grafo:
            self.grafo[v] = []
        self.grafo[v].append(w)
        self.vertices.add(v)
        self.vertices.add(w)

    def adicionar_interesses(self, usuario: str, interesses: list):
        self.interesses[usuario] = set(interesses)

    def recomendar_usuarios(self, usuario):
        if usuario not in self.interesses:
            return []

        interesses_usuario = self.interesses[usuario]
        recomendacoes = []

        g = nx.DiGraph()
        for v, conexoes in self.grafo.items():
            for w in conexoes:
                g.add_edge(v, w)
        cfc = list(nx.strongly_connected_components(g))
        cluster_usuario = next((c for c in cfc if usuario in c), set())

        for outro_usuario, interesses_outro in self.interesses.items():
            if outro_usuario != usuario and outro_usuario not in self.grafo.get(usuario, []):
                interesses_comuns = interesses_usuario & interesses_outro
                mesmo_cluster = outro_usuario in cluster_usuario
                if interesses_comuns or mesmo_cluster:
                    score = len(interesses_comuns) + (1 if mesmo_cluster else 0)
                    recomendacoes.append((outro_usuario, score, interesses_comuns, mesmo_cluster))

        # Ordenar recomendações por score (interesses + CFC)
        recomendacoes.sort(key=lambda x: x[1], reverse=True)
        return recomendacoes

    def gerar_grafo_visual(self):
        g = nx.DiGraph()  
        
        for v, conexoes in self.grafo.items():
            for w in conexoes:
                g.add_edge(v, w)

        pos = nx.spring_layout(g) 

        plt.figure(figsize=(10, 8))
        nx.draw(
            g, 
            pos, 
            with_labels=True, 
            node_color="skyblue", 
            node_size=2000, 
            font_size=10, 
            font_weight="bold", 
            arrowsize=20
        )

        nodes = nx.draw_networkx_nodes(g, pos, node_color="skyblue", node_size=2000)
        cursor = mplcursors.cursor(nodes, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            node = list(g.nodes())[sel.index]
            interesses = self.interesses.get(node, [])
            recomendacoes = self.recomendar_usuarios(node)

            texto = f"{node}\nInteresses: {', '.join(interesses)}"
            if recomendacoes:
                texto += f"\n\nRecomendações de amizade:"
                for usuario, score, interesses_comuns, mesmo_cluster in recomendacoes:
                    tipo = " (mesmo cluster)" if mesmo_cluster else ""
                    texto += f"\n {usuario}{tipo} ({len(interesses_comuns)} interesses em comum: {', '.join(interesses_comuns)})"
            else:
                texto += "\n\nSem recomendações."

            sel.annotation.set_text(texto)
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

        plt.title("Grafo Interativo com Recomendações")
        plt.show()

grafo = Grafo()

grafo.adicionar_aresta("Ana", "Bia")
grafo.adicionar_aresta("Bia", "Pedro")
grafo.adicionar_aresta("Pedro", "Ana")
grafo.adicionar_aresta("Bia", "Lucas")
grafo.adicionar_aresta("Lucas", "Ana")
grafo.adicionar_aresta("Lucas", "Joao")
grafo.adicionar_aresta("Joao", "Ze")
grafo.adicionar_aresta("Ze", "Bruna")
grafo.adicionar_aresta("Bruna", "Joao")
grafo.adicionar_aresta("Marcos", "Carla")
grafo.adicionar_aresta("Carla", "Diego")
grafo.adicionar_aresta("Diego", "Lucas")
grafo.adicionar_aresta("Lucas", "Marcos")
grafo.adicionar_aresta("Sophia", "Ana")
grafo.adicionar_aresta("Ana", "Sophia")
grafo.adicionar_aresta("Sophia", "Carla")
grafo.adicionar_aresta("Diego", "Bruna")

grafo.adicionar_interesses("Ana", ["música", "viagem", "livros", "fotografia"])
grafo.adicionar_interesses("Bia", ["música", "culinária", "moda"])
grafo.adicionar_interesses("Pedro", ["esportes", "viagem", "tecnologia"])
grafo.adicionar_interesses("Lucas", ["tecnologia", "música", "filmes"])
grafo.adicionar_interesses("Joao", ["culinária", "livros", "história"])
grafo.adicionar_interesses("Ze", ["esportes", "tecnologia", "viagem"])
grafo.adicionar_interesses("Bruna", ["viagem", "livros", "arte"])
grafo.adicionar_interesses("Marcos", ["fotografia", "música", "tecnologia"])
grafo.adicionar_interesses("Carla", ["moda", "arte", "fotografia"])
grafo.adicionar_interesses("Diego", ["esportes", "fotografia", "filmes", "viagem", "livros"])
grafo.adicionar_interesses("Sophia", ["história", "livros", "fotografia"])

grafo.gerar_grafo_visual()