"""
2019253022 홍한울
"""
def generate_graph_and_init_cluster(filename):
   ad_list = dict()
   file_input = open(filename , 'r')

   for line in file_input:
      v1, v2 = line.strip().split('\t')

      if v1 not in ad_list.keys():
         ad_list[v1] = set()

      if v2 not in ad_list.keys():
         ad_list[v2] = set()
      
      ad_list[v1].add(v2)
      ad_list[v2].add(v1)


   clusters = [set([node]) for node in ad_list]      
      
   return ad_list, clusters


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

   #select 2 clusters
    for cluster1 in clusters:
        for cluster2 in clusters:
            if cluster1 != cluster2:
                # cluster간 연결 확인
                for v1 in cluster1:
                    for v2 in cluster2:
                        if v2 in graph[v1]:
                            if {v1,v2} not in edges_between_clusters:
                            
                             edges_between_clusters.append({v1, v2})

    return edges_between_clusters


def calculate_density(graph, clusters):

    # 해당 클러스터 
    n = len(clusters)


    return 0

final_clusters =[]
threshold = 0.4

def hierarchical_algorithm(graph, cluster):
    edge_list = find_edges_between_clusters(graph,cluster)


    
    return 0

def main():
 global final_clusters
 input_file  = 'test.txt'
   #output_file = 'assignment6_output.txt'
 graph, size_1_clusters = generate_graph_and_init_cluster(input_file)
 hierarchical_algorithm(graph, size_1_clusters)

if __name__ == '__main__':
    main()

