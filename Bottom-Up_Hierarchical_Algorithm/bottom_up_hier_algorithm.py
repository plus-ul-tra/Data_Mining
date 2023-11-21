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


final_clusters =[]
def main():
 global final_clusters
 input_file  = '1.txt'
   #output_file = 'assignment6_output.txt'
 initial_forest, size_1_clusters = generate_graph_and_init_cluster(input_file)

if __name__ == '__main__':
    main()

