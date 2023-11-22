""""
2019253022_홍한울
"""

import math
import time
import sys
def preprocessing_output_file(filename):
   data_file = open(filename,'r')
   data_matrix =[]
   
   for i, line in enumerate(data_file):
    objects = line.split(": ")
    numbers = objects[1]
    objects_list = [int(number) for number in numbers.split()]
    row = [i + 1] + objects_list
    data_matrix.append(row)
      
   
   return data_matrix

def preprocessing_ground_file(filename):
   data_file = open(filename, 'r')
   index_and_cluster_matrix =[]
   result = dict()
   data_matrix =[]
   
   # [cluster , object]쌍 생성
   for i, line in enumerate(data_file):
      cluster = int(line.split()[0])
      row = [cluster,i]
      index_and_cluster_matrix.append(row)
    
    #같은 cluster끼리 정리
   for row in index_and_cluster_matrix:
     index = row[0]
     value = row[1]
    
     if index in result:
        result[index].append(value)
     else:
        result[index] = [value]

   if -1 in result:
      del result[-1]
 # 결과를 matrix 형태로 만들기
   data_matrix = [[index] + values for index, values in result.items()]

   return data_matrix


def calculate_in_same_cluster(cluster, a,b):
   
   # a,b 같은 cluster 존재:1, 아님:0
   for row in cluster:
        if a in row[1:] and b in row[1:]:
            return 1

   return 0


def generate_incident_matrix(cluster):
   incident_matrix =[]

   for i in range(500):
      row=[]
      for j in range(500):
         row.append(calculate_in_same_cluster(cluster, i ,j))
      incident_matrix.append(row)
   


   return incident_matrix


def calculate_jaccard_index(c, p):
   ss,sd,ds = 0,0,0
   #incident_matrix 생성
   incident_matrix_of_c = generate_incident_matrix(c)
   incident_matrix_of_p = generate_incident_matrix(p)

   for i in range(500):
      for j in range(500):
         
         if incident_matrix_of_c[i][j] ==1 and incident_matrix_of_p[i][j]==1:
            ss+= 1
         elif incident_matrix_of_c[i][j] == 1 and incident_matrix_of_p[i][j]== 0:
            sd += 1
         elif incident_matrix_of_c[i][j] == 0 and incident_matrix_of_p[i][j]== 1:
            ds += 1
   jaccard_index = ss / (ss+sd+ds)
   return jaccard_index



def main():
 clustering_algorithm_result = sys.argv[1]
 ground_truth_file = sys.argv[2]
 # read assignment3_output.txt -> clustering Algorithm
 result_clustering = preprocessing_output_file(clustering_algorithm_result)
 # read assignment5_input.txt -> ground_truth
 ground_truth = preprocessing_ground_file(ground_truth_file)
 start_time = time.time()
 jaccard_index = calculate_jaccard_index(result_clustering,ground_truth)
 end_time = time.time()

 print("elapsed_time :" + str(end_time-start_time))
 print(jaccard_index)


#print(jaccard_index)






if __name__ == '__main__':
    main()