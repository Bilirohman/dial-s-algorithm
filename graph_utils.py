# graph_utils.py
from collections import defaultdict


class Graph:
    """
    Kelas untuk merepresentasikan struktur data graf.
    Menggunakan defaultdict untuk menyimpan adjacency list.
    """

    def __init__(self):
        # Adjacency list: node -> list of (neighbor, weight)
        self.adj = defaultdict(list)
        # Set untuk menyimpan semua node unik
        self.nodes = set()
        # Menyimpan bobot maksimum untuk inisialisasi bucket di Algoritma Dial
        self.max_weight = 0

    def add_node(self, node_name):
        """Menambahkan node ke dalam graf."""
        if node_name:
            self.nodes.add(node_name)

    def add_edge(self, u, v, weight):
        """Menambahkan edge berarah dari u ke v dengan bobot."""
        if u and v and weight is not None:
            # Pastikan node ada di dalam set nodes
            self.nodes.add(u)
            self.nodes.add(v)

            # Tambahkan edge ke adjacency list
            self.adj[u].append((v, weight))

            # Perbarui bobot maksimum yang pernah ditemui
            if weight > self.max_weight:
                self.max_weight = weight

    def get_nodes(self):
        """Mengembalikan daftar node yang telah diurutkan."""
        return sorted(list(self.nodes))
