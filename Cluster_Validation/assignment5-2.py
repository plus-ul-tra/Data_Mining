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
    data_matrix.append(objects_list)
      
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
   data_matrix = [values for values in result.values()]

   return data_matrix


def calculate_f_measure(cluster_x, ground_y):
   highest_f_score_list =list()

   for x in cluster_x:
      max=0
      cluster_set =()
      cluster_set = set(x)
      for y in ground_y:
         
         ground_set = set()
         ground_set = set(y)
         intersection_set = cluster_set.intersection(ground_set)
         intersection_count = len(intersection_set)

         recall = intersection_count/len(cluster_set)
         precision = intersection_count/len(ground_set)
         if (recall+precision) != 0:
          f_score = 2*recall*precision/(recall+precision)
         else:
            f_score = 0
         if max < f_score:
             max = f_score 
      highest_f_score_list.append(max)
   
   total_sum = sum(highest_f_score_list)
   average = total_sum/len(highest_f_score_list)
   return average


def main():
 clustering_algorithm_result = sys.argv[1]
 ground_truth_file = sys.argv[2]
 # read assignment3_output.txt -> clustering Algorithm
 result_clustering = preprocessing_output_file(clustering_algorithm_result)
 # read assignment5_input.txt -> ground_truth
 ground_truth = preprocessing_ground_file(ground_truth_file)
 start_time = time.time()
 average = calculate_f_measure(result_clustering,ground_truth)
 end_time = time.time()

 print("elapsed_time :" + str(end_time-start_time))
 print(average)



if __name__ == '__main__':
    main()