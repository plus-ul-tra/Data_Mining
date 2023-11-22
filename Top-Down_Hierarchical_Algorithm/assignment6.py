"""
2019253022홍한울
"""
import time
import sys

def generate_adjacency_list(filename):
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
         
      
   return ad_list

# 간선을 cut한다 = 두 노드 n1,n2의 adj_set에서 서로를 지운다. -> cut의 구현
def dfs(graph, node, visited, connected_group):
    visited[node] = True
    connected_group.add(node)

    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, connected_group)


def find_connected_groups(graph):
    visited = {node: False for node in graph}
    connected_groups = []

    for node in graph:
        if not visited[node]:
            connected_group = set()
            dfs(graph, node, visited, connected_group)
            connected_groups.append(connected_group)

    return connected_groups


def update_adjacency_list(com_list, graph):
   copy = dict(graph)
   for k in graph:
         if k not in com_list:
            del copy[k]

   return copy


def calculate_jaccard_index(sub_graph):
   min_index = float('inf')
   jaccard_index = 0

   for k1,v1 in sub_graph.items():
      for k2,v2 in sub_graph.items():
         if k1 != k2 and k2 in v1 :

            union_size = len(v1.union(v2))
            intersection_size = len(v1.intersection(v2))
            jaccard_index = intersection_size/union_size
            if min_index > jaccard_index:
               min_index = jaccard_index

               del_vertex1 = k1
               del_vertex2 = k2 

   return del_vertex1, del_vertex2


def edge_cutting(sub_graph):

   # jaccard index 가 최소인 관계의 v1 ,v2 => edge 제거
   v1,v2 = calculate_jaccard_index(sub_graph)

   value_set = sub_graph.get(v1,set())
   value_set.discard(v2)
   sub_graph[v1] = value_set

   value_set2 = sub_graph.get(v2,set())
   value_set2.discard(v1)
   sub_graph[v2] = value_set2

   return sub_graph

def calculate_density(group_list,adjacency_list):
   total=0
   num_of_vertex = len(group_list)
   for k,v in adjacency_list.items():
      if k in group_list:
         total += len(v)
   
   if (num_of_vertex * (num_of_vertex - 1)) > 0:
    density = total / (num_of_vertex * (num_of_vertex - 1))
    # 계산하러 왔다는 것은 무조건 2개의 sub graph로 되어있는 상태
   
   return density

def recusive_sequence(connected_sub_graph):
   global cluster

   #edge cutting 결과
   result_graph_adj_list = edge_cutting(connected_sub_graph)
   
   #그룹의 vertex들만 나타낸 것
   after_cutting_graph_groups = find_connected_groups(result_graph_adj_list)
   
   if len(after_cutting_graph_groups) == 2:
      # cutting 된 경우 
      # density 계산
      for i  in range(2):

       density = calculate_density(after_cutting_graph_groups[i], result_graph_adj_list)
       
       #density와 size모두 만족 한 경우
       if density > 0.4 and len(after_cutting_graph_groups[i])>=10:
           cluster.append(after_cutting_graph_groups[i])
           return 0
         
         #  print(after_cutting_graph_groups)

       else:
          # grouplist,
          new_connected = update_adjacency_list(after_cutting_graph_groups[i],result_graph_adj_list)
          recusive_sequence(new_connected)
         
          

   else :
      recusive_sequence(result_graph_adj_list)
      # cutting 되지 않은 경우

   return 0


def hierarchical_algorithm(graph):

   # copy

    # number of nodes = 2인 component는 jaccard index에서 disconnected되고 어처피 사라지므로 미리 버린다.
    # 3개짜리 부터는 해봐야 안다.

    # 컴포넌트들의 리스트
   components_list = find_connected_groups(graph)
   filtered_components_list = [s for s in components_list if len(s) != 2]
   
   #시작 2000여개 시작
   for i in range(len(filtered_components_list)):

    connected_sub_graph = update_adjacency_list(filtered_components_list[i], graph)

   recusive_sequence(connected_sub_graph)

   #끓겨 있을 수도 아닐 수도 있는 상태
   #인접 리스트

   return 0

# key= node, value = adjacency node set

def output_to_file(result,filename):
    file = open(filename, 'w')

    for data in result:
        s = str(len(data)) + ":" + str(data)
        file.write(s)

    file.close()

cluster = []
def main():
 global cluster

 input_file  = 'assignment6_input.txt'
 output_file = 'assignment6_output.txt'
 initial_forest = generate_adjacency_list(input_file)
 start_time = time.time()
 hierarchical_algorithm(initial_forest)
 end_time = time.time()
 output_to_file(cluster,output_file)
 print("elapsed_time :" + str(end_time-start_time))


if __name__ == '__main__':
    main()



