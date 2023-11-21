def calculate_jaccard_index(graph, v1, v2):
    neighbors_v1 = graph[v1]
    neighbors_v2 = graph[v2]

    union_size = len(neighbors_v1.union(neighbors_v2))
    intersection_size = len(neighbors_v1.intersection(neighbors_v2))

    if union_size > 0:
        jaccard_index = intersection_size / union_size
        return jaccard_index
    else:
        return 0


def find_edges_between_clusters(graph, clusters):
    edges_between_clusters = []

    for cluster1 in clusters:
        for cluster2 in clusters:
            if cluster1 != cluster2:
                for v1 in cluster1:
                    for v2 in cluster2:
                        if v2 in graph[v1]:
                            edges_between_clusters.append((v1, v2))

    return edges_between_clusters


def merge_clusters(graph, clusters):
    max_jaccard_index = 0
    max_jaccard_pair = None

    for cluster1 in clusters:
        for cluster2 in clusters:
            if cluster1 != cluster2:
                for v1 in cluster1:
                    for v2 in cluster2:
                        jaccard_index = calculate_jaccard_index(graph, v1, v2)
                        if jaccard_index > max_jaccard_index:
                            max_jaccard_index = jaccard_index
                            max_jaccard_pair = (cluster1, cluster2, v1, v2)

    if max_jaccard_pair:
        merged_cluster = set(max_jaccard_pair[0]).union(set(max_jaccard_pair[1]))
        return merged_cluster, max_jaccard_pair[2], max_jaccard_pair[3]
    else:
        return None, None, None


def hierarchical_algorithm(graph, density_threshold):
    clusters = [set([node]) for node in graph]

    while len(clusters) > 1:
        edges_between_clusters = find_edges_between_clusters(graph, clusters)

        if not edges_between_clusters:
            break

        v1, v2 = edges_between_clusters[0]

        clusters.remove({v1})
        clusters.remove({v2})

        merged_cluster, merged_v1, merged_v2 = merge_clusters(graph, clusters)

        if merged_cluster:
            clusters.append(merged_cluster)

    candidate_clusters = [cluster for cluster in clusters if len(cluster) > 1]

    final_clusters = []
    for candidate_cluster in candidate_clusters:
        is_superset = all(
            not (candidate_cluster.issuperset(other) and candidate_cluster != other)
            for other in candidate_clusters
        )
        if is_superset:
            final_clusters.append(candidate_cluster)

    return final_clusters


# 예시 그래프 (인접 리스트 형식)
example_graph = {
    1: {2, 3},
    2: {1, 3, 4},
    3: {1, 2, 4},
    4: {2, 3, 5},
    5: {4}
}

# 밀도 임계값 설정
threshold = 0.4

# 계층적 알고리즘 실행
result_clusters = hierarchical_algorithm(example_graph, threshold)

print("Final Clusters:")
for cluster in result_clusters:
    print(cluster)
