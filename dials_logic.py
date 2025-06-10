# dials_logic.py
import heapq


def dials_algorithm(graph, start_node):
    """
    Implementasi Algoritma Dial menggunakan generator (yield) untuk visualisasi.

    Args:
        graph (Graph): Objek graf yang berisi nodes, adj, dan max_weight.
        start_node (str): Node awal.

    Yields:
        dict: Kamus yang berisi keadaan algoritma di setiap langkah.
    """
    # Inisialisasi jarak: tak terhingga untuk semua node
    distances = {node: float("inf") for node in graph.get_nodes()}
    # Jarak ke node awal adalah 0
    distances[start_node] = 0

    # Inisialisasi buckets. Ukurannya adalah (jumlah node * bobot maks + 1)
    # Ini adalah batas atas yang aman untuk jarak terpendek.
    max_possible_dist = len(graph.get_nodes()) * graph.max_weight
    buckets = [[] for _ in range(max_possible_dist + 1)]

    # Masukkan node awal ke bucket pertama (bucket 0)
    buckets[0].append(start_node)

    # Langkah awal: Inisialisasi
    yield {
        "description": f"Inisialisasi: Jarak ke '{start_node}' diatur ke 0, lainnya ∞. Node '{start_node}' dimasukkan ke bucket 0.",
        "distances": distances.copy(),
        "buckets": [b[:] for b in buckets],
        "current_node": start_node,
        "neighbor": None,
        "path": [],
        "final": False,
    }

    bucket_idx = 0
    while bucket_idx <= max_possible_dist:
        # Cari bucket tidak kosong berikutnya untuk efisiensi
        while bucket_idx <= max_possible_dist and not buckets[bucket_idx]:
            bucket_idx += 1

        if bucket_idx > max_possible_dist:
            break

        # Proses semua node di bucket saat ini
        while buckets[bucket_idx]:
            u = buckets[bucket_idx].pop(0)  # Ambil node dari bucket

            # Jika kita menemukan jalur yang lebih pendek ke u sebelumnya, abaikan
            if distances[u] < bucket_idx:
                continue

            yield {
                "description": f"Mengambil node '{u}' dari bucket {bucket_idx}. Jarak saat ini: {distances[u]}.",
                "distances": distances.copy(),
                "buckets": [b[:] for b in buckets],
                "current_node": u,
                "neighbor": None,
                "path": [],
                "final": False,
            }

            # Lihat semua tetangga dari u
            for v, weight in graph.adj.get(u, []):
                yield {
                    "description": f"Memeriksa tetangga '{v}' dari '{u}' dengan bobot {weight}.",
                    "distances": distances.copy(),
                    "buckets": [b[:] for b in buckets],
                    "current_node": u,
                    "neighbor": v,
                    "path": [],
                    "final": False,
                }

                # Relaksasi edge
                if distances[u] + weight < distances[v]:
                    old_dist = distances[v]
                    # Hapus v dari bucket lama jika ada (opsional, karena kita punya pengecekan di atas)
                    # Di implementasi sederhana, kita bisa langsung menambahkan.

                    # Perbarui jarak
                    distances[v] = distances[u] + weight

                    # Masukkan v ke bucket baru yang sesuai
                    buckets[distances[v]].append(v)

                    yield {
                        "description": f"Relaksasi edge ({u} -> {v}): Jarak ke '{v}' diperbarui dari {old_dist} menjadi {distances[v]}. '{v}' dimasukkan ke bucket {distances[v]}.",
                        "distances": distances.copy(),
                        "buckets": [b[:] for b in buckets],
                        "current_node": u,
                        "neighbor": v,
                        "path": [],
                        "final": False,
                    }

    # Langkah akhir: Menampilkan hasil
    yield {
        "description": f"Algoritma selesai. Jarak terpendek dari '{start_node}' telah ditemukan.",
        "distances": distances.copy(),
        "buckets": [b[:] for b in buckets],
        "current_node": None,
        "neighbor": None,
        "path": list(distances.keys()),  # Menandakan semua node untuk pewarnaan akhir
        "final": True,
    }
