"""
2019253022 홍한울
"""
import copy
import time
import sys
def generate_graph_and_init_cluster(filename):
   ad_list = dict()
   file_input = open(filename , 'r')
   all_edges_list_with_index =[]

   for line in file_input:
      v1, v2 = line.strip().split('\t')

      if v1 not in ad_list.keys():
         ad_list[v1] = set()

      if v2 not in ad_list.keys():
         ad_list[v2] = set()
      
      ad_list[v1].add(v2)
      ad_list[v2].add(v1)


   clusters = [set([node]) for node in ad_list] 
   file_input.seek(0)
   for line in file_input:
        v1,v2 = line.strip().split('\t')
        jaccard_index = calculate_jaccard_index(ad_list,v1,v2)
        all_edges_list_with_index.append((v1,v2,jaccard_index))  

      
      # 인접리스트, 단일 클러스터
   return ad_list, clusters, all_edges_list_with_index



def calculate_jaccard_index(graph, v1, v2):
    neighbors_v1 = graph[v1]
    neighbors_v2 = graph[v2]

    union_size = len(neighbors_v1.union(neighbors_v2))
    intersection_size = len(neighbors_v1.intersection(neighbors_v2))

    if union_size > 0:
        jaccard_index = intersection_size / union_size

        return round(jaccard_index,3)


def calculate_density(cluster, graph):
    # 클러스터 내의 node, edge에 관한 density.
    total_edges = 0
    total_node = len(cluster) * (len(cluster) - 1)

    for node in cluster:
        # 해당 노드와 연결된 노드 중 클러스터 내의 노드만 고려
        edges = [neighbor for neighbor in graph[node] if neighbor in set(cluster)]
        total_edges += len(edges)

    if total_node > 0:
        density = total_edges / total_node
        return density >= 0.4


def merge_clusters(graph,clusters, edge_list):
    #합칠 cluster
    new_cluster =[]
    copy_for_delete = copy.deepcopy(clusters)
    ex_list =[]

    while copy_for_delete:

        for cluster in clusters:
                for v1 in cluster:
                    #다른 클러스터와 연결된 edges
                    filtered_tuples = [tpl for tpl in edge_list if (tpl[0] == v1 and tpl[1] not in cluster) or (tpl[1] == v1 and tpl[0] not in cluster)]
                
                if filtered_tuples:
                    # 그 edge중 max 찾기        
                    max_jaccard_tuple = max(filtered_tuples, key=lambda x: x[2])
                    # jaccard index가 0.1보다 작은 경우 스킵
                    if max_jaccard_tuple[2] < 0.1:
                        copy_for_delete.pop()
                        continue

                    # max tuple 중 cluster가 아닌 노드 선택
                    if max_jaccard_tuple[0] in cluster:
                        other_node = max_jaccard_tuple[1]
                    else: other_node = max_jaccard_tuple[0]

                    # 새롭게 merge된 경우에 반영 (중복X)
                 
                    for s in clusters:
                            if other_node in s:
                                merge_set = cluster.union(s)
                                if len(merge_set) >= 10 :
                                    density =calculate_density(merge_set,graph)
                                    if density:
                                        candidate_clusters.append(merge_set)
                                new_cluster.append(merge_set)
                                ex_list.append(cluster)
                                ex_list.append(s)
                                break 
                          
                    copy_for_delete.pop()

                else:
                    copy_for_delete.pop()
                    continue



    if new_cluster:
        return new_cluster
    else:
        return 0
    

def gene_size2(graph, clusters, edge_list):
    ex_list =[]
    two_clusters = []

    for v1 in clusters:
        real_v1 = list(v1)
        real_real_v1 = real_v1[0]
        if real_real_v1 not in ex_list:
            filtered_tuples = [tpl for tpl in edge_list if real_real_v1 in tpl]
            if filtered_tuples:
                max_jaccard_tuple = max(filtered_tuples, key=lambda x: x[2])
                if max_jaccard_tuple[2]>=0.1 and max_jaccard_tuple[0] not in ex_list and max_jaccard_tuple[1] not in ex_list:
                    new_set = set([max_jaccard_tuple[0],max_jaccard_tuple[1]])
                    two_clusters.append(new_set)
                    ex_list.append(max_jaccard_tuple[0])
                    ex_list.append(max_jaccard_tuple[1])

    return two_clusters


def bottom_up_hierarchical_algorithm(graph, clusters, edge_list_with_index):
        clusters = gene_size2(graph, clusters, edge_list_with_index)

        while True:
            new_clusters = merge_clusters(graph, clusters,edge_list_with_index)
            if new_clusters:
                clusters =new_clusters
            else:
                break

        return clusters

candidate_clusters =[]
threshold = 0.4

def find_supersets(sets):
    supersets = []

    for i, set1 in enumerate(sets):
        is_superset = all(set1.issuperset(set2) for j, set2 in enumerate(sets) if i != j)
        
        if is_superset:
            supersets.append(set1)

    return supersets
def output(filename):
    sorted_clusters = sorted(candidate_clusters, key=len, reverse=True)
    with open(filename, 'w') as file:
        for cluster in sorted_clusters:
            file.write(f"{len(cluster)}: {' '.join(cluster)}\n")
    return 0

def main():
 global candidate_clusters
 input_file  = 'input_data.txt'
 output_file = 'result'
 start_time = time.time()
 graph, size_1_clusters, edge_list_with_index  = generate_graph_and_init_cluster(input_file)
 bottom_up_hierarchical_algorithm(graph, size_1_clusters, edge_list_with_index)
 output(output_file)
 end_time = time.time()
 elapsed_time = end_time - start_time
 print("elapsed time : {}",elapsed_time)

if __name__ == '__main__':
    main()

