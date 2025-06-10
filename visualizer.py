# visualizer.py
import graphviz


def create_graph_viz(graph_obj, state):
    """
    Membuat visualisasi graf menggunakan Graphviz berdasarkan keadaan algoritma.

    Args:
        graph_obj (Graph): Objek graf.
        state (dict): Keadaan saat ini dari algoritma.

    Returns:
        graphviz.Digraph: Objek graf yang dapat dirender.
    """
    dot = graphviz.Digraph(comment="Graf Jalur Terpendek")
    dot.attr(rankdir="LR", splines="true", overlap="false", fontsize="12")
    dot.attr("node", shape="circle", style="filled", color="skyblue", fontcolor="black")
    dot.attr("edge", color="gray", fontcolor="darkgray")

    distances = state.get("distances", {})
    current_u = state.get("current_node")
    current_v = state.get("neighbor")
    final_path_nodes = state.get("path", []) if state.get("final") else []

    # Tambahkan nodes
    for node in graph_obj.get_nodes():
        dist_label = distances.get(node, "∞")
        label = f"{node}\n(d={dist_label})"

        node_color = "lightgray"  # Warna default
        if state.get("final"):
            if distances.get(node, float("inf")) != float("inf"):
                node_color = "lightgreen"  # Warna hasil akhir
        elif node == current_u:
            node_color = "orange"  # Node yang sedang diproses
        elif node == current_v:
            node_color = "yellow"  # Tetangga yang sedang diperiksa

        dot.node(node, label=label, color=node_color)

    # Tambahkan edges
    for u in graph_obj.adj:
        for v, weight in graph_obj.adj[u]:
            edge_color = "gray"
            penwidth = "1.0"

            if u == current_u and v == current_v:
                edge_color = "red"  # Edge yang sedang direlaksasi
                penwidth = "2.5"

            dot.edge(u, v, label=str(weight), color=edge_color, penwidth=penwidth)

    return dot
