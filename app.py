# app.py
import streamlit as st
import pandas as pd
from graph_utils import Graph
from dials_logic import dials_algorithm
from visualizer import create_graph_viz

# --- Konfigurasi Halaman & Inisialisasi State ---
st.set_page_config(page_title="Visualisasi Algoritma Dial", layout="wide")

# Inisialisasi session state untuk menyimpan data graf dan status algoritma
if "graph" not in st.session_state:
    st.session_state.graph = Graph()
if "steps" not in st.session_state:
    st.session_state.steps = []
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "algorithm_running" not in st.session_state:
    st.session_state.algorithm_running = False


# Fungsi untuk mereset semua state
def reset_all():
    st.session_state.graph = Graph()
    st.session_state.steps = []
    st.session_state.current_step = 0
    st.session_state.algorithm_running = False


# --- UI Sidebar untuk Kontrol ---
with st.sidebar:
    st.title("Kontrol Visualisasi")
    st.markdown("---")

    st.header("1. Bangun Graf Anda")

    # Input untuk menambah node
    new_node = st.text_input("Nama Node Baru", placeholder="Contoh: A")
    if st.button("➕ Tambah Node"):
        if new_node:
            st.session_state.graph.add_node(new_node)
            st.success(f"Node '{new_node}' berhasil ditambahkan.")
        else:
            st.warning("Nama node tidak boleh kosong.")

    # Input untuk menambah edge
    nodes = st.session_state.graph.get_nodes()
    if len(nodes) >= 2:
        col1, col2, col3 = st.columns(3)
        with col1:
            u_node = st.selectbox("Dari Node", options=nodes, key="u_node")
        with col2:
            v_node = st.selectbox("Ke Node", options=nodes, key="v_node")
        with col3:
            weight = st.number_input("Bobot", min_value=0, step=1, key="weight")

        if st.button("🔗 Tambah Edge"):
            if u_node != v_node:
                st.session_state.graph.add_edge(u_node, v_node, int(weight))
                st.success(
                    f"Edge dari '{u_node}' ke '{v_node}' dengan bobot {weight} ditambahkan."
                )
            else:
                st.warning("Node awal dan tujuan tidak boleh sama.")
    else:
        st.info("Tambahkan setidaknya dua node untuk membuat edge.")

    st.markdown("---")
    st.header("2. Jalankan Algoritma")

    if nodes:
        start_node = st.selectbox("Pilih Node Awal", options=nodes)

        if st.button("🚀 Jalankan Algoritma Dial", type="primary"):
            st.session_state.steps = list(
                dials_algorithm(st.session_state.graph, start_node)
            )
            st.session_state.current_step = 0
            st.session_state.algorithm_running = True
    else:
        st.warning("Graf masih kosong. Tambahkan node dan edge terlebih dahulu.")

    st.markdown("---")
    if st.button("🔄 Reset Graf & Visualisasi"):
        reset_all()
        st.rerun()


# --- UI Area Utama untuk Tampilan ---
st.title("Visualisasi Interaktif Algoritma Dial")
st.markdown(
    """
Algoritma Dial adalah sebuah algoritma pencarian jalur terpendek yang dioptimalkan untuk graf dengan **bobot edge berupa bilangan bulat non-negatif**. Algoritma ini mirip dengan Dijkstra tetapi menggunakan struktur data "bucket" (ember) untuk menyimpan node yang akan dikunjungi. Setiap bucket `i` menyimpan node-node dengan jarak tentatif `i` dari sumber. Ini membuatnya sangat efisien ketika bobot maksimum (`C`) tidak terlalu besar.
"""
)

if not st.session_state.algorithm_running and not st.session_state.graph.get_nodes():
    st.info(
        "Selamat datang! Mulailah dengan menambahkan node dan edge pada panel kontrol di sebelah kiri."
    )

# Pisahkan layout menjadi dua kolom
col_viz, col_detail = st.columns([0.6, 0.4])

with col_viz:
    st.subheader("Visualisasi Graf")
    graph_placeholder = st.empty()

with col_detail:
    st.subheader("Detail Langkah Algoritma")
    desc_placeholder = st.empty()
    dist_placeholder = st.empty()
    bucket_placeholder = st.empty()


# --- Logika Rendering ---
if st.session_state.algorithm_running and st.session_state.steps:
    # Navigasi langkah
    step_info = st.session_state.steps[st.session_state.current_step]

    # Tombol Navigasi
    col1, col2, col3 = st.columns([1, 1, 5])
    with col1:
        if st.button("⬅️ Kembali") and st.session_state.current_step > 0:
            st.session_state.current_step -= 1
            st.rerun()
    with col2:
        if (
            st.button("Lanjut ➡️")
            and st.session_state.current_step < len(st.session_state.steps) - 1
        ):
            st.session_state.current_step += 1
            st.rerun()

    with col3:
        st.write(
            f"Langkah: **{st.session_state.current_step + 1} / {len(st.session_state.steps)}**"
        )

    # Render Visualisasi Graf
    with graph_placeholder.container():
        viz = create_graph_viz(st.session_state.graph, step_info)
        st.graphviz_chart(viz)

    # Render Detail Langkah
    description = step_info["description"]
    distances = step_info["distances"]
    buckets = step_info["buckets"]

    desc_placeholder.info(f"**Penjelasan:** {description}")

    # Tampilkan tabel jarak
    dist_df = pd.DataFrame(
        list(distances.items()), columns=["Node", "Jarak Terpendek"]
    ).set_index("Node")
    dist_placeholder.dataframe(dist_df, use_container_width=True)

    # Tampilkan status buckets
    bucket_str_list = []
    for i, bucket in enumerate(buckets):
        if bucket:
            bucket_str_list.append(f"**Bucket {i}:** `{', '.join(map(str, bucket))}`")

    if bucket_str_list:
        bucket_placeholder.markdown(
            "#### Status Buckets\n" + "\n".join(bucket_str_list)
        )
    else:
        bucket_placeholder.markdown("#### Status Buckets\nSemua bucket kosong.")

    if step_info.get("final", False):
        st.balloons()
        st.success("Pencarian jalur terpendek telah selesai!")

elif st.session_state.graph.get_nodes():
    # Tampilkan graf awal sebelum algoritma dijalankan
    initial_state = {
        "distances": {node: "∞" for node in st.session_state.graph.get_nodes()}
    }
    viz = create_graph_viz(st.session_state.graph, initial_state)
    graph_placeholder.graphviz_chart(viz)
    desc_placeholder.info(
        "Graf Anda telah dibuat. Pilih node awal dan jalankan algoritma dari sidebar."
    )
