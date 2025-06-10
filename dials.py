INF = 999999999  # Representasi tak hingga

def print_buckets_state(buckets):
    print("\n== Keadaan Buckets Saat Ini ==")
    for i, bucket in enumerate(buckets):
        if bucket:
            print(f"Bucket[{i}]: {bucket}")
    print()


def dial_algorithm(graph, V, src, max_weight):
    # Inisialisasi jarak ke semua simpul sebagai tak hingga
    dist = [INF] * V
    dist[src] = 0

    # Membuat bucket list kosong sebanyak max_weight * V + 1
    buckets = [[] for _ in range(max_weight * V + 1)]
    buckets[0].append(src)  # Masukkan simpul sumber ke bucket 0

    idx = 0  # Mulai dari bucket ke-0
    step = 1
    while idx < len(buckets):
        if len(buckets[idx]) == 0:
            idx += 1
            continue

        # Ambil simpul dari bucket sekarang
        u = buckets[idx][0]
        buckets[idx] = buckets[idx][1:]

        print(f"Langkah {step}:")
        print(
            f"  - Memproses node {u} dari bucket[{idx}] dengan jarak saat ini {dist[u]}"
        )
        print_buckets_state(buckets)

        for neighbor in graph[u]:
            v = neighbor[0]
            weight = neighbor[1]

            if dist[v] > dist[u] + weight:
                old_distance = dist[v]
                new_distance = dist[u] + weight
                dist[v] = new_distance

                if old_distance != INF:
                    try:
                        buckets[old_distance].remove(v)
                        print(f"    > Menghapus node {v} dari bucket[{old_distance}]")
                    except ValueError:
                        pass  # Bisa diabaikan jika tidak ada

                buckets[new_distance].append(v)
                print(
                    f"    > Menambahkan node {v} ke bucket[{new_distance}], jarak baru = {new_distance}"
                )

        step += 1

    print("\n== Jarak Minimum Akhir dari Sumber ==")
    for i in range(V):
        print(f"Node {i}: {dist[i]}")

    return dist


if __name__ == "__main__":
    V = 6
    src = 0
    max_weight = 5  # Berat maksimum antar edge dalam graf

    # Representasi graf tak berarah berbobot:
    # Format: graph[u] = [[v, berat], ...]
    graph = [
        [[1, 2], [2, 4]],  # Node 0
        [[0, 2], [2, 1], [3, 7]],  # Node 1
        [[0, 4], [1, 1], [3, 3], [4, 1]],  # Node 2
        [[1, 7], [2, 3], [4, 2], [5, 5]],  # Node 3
        [[2, 1], [3, 2], [5, 1]],  # Node 4
        [[3, 5], [4, 1]],  # Node 5
    ]

    dial_algorithm(graph, V, src, max_weight)
