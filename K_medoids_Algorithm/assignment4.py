""""
2019253022_홍한울
"""
import math
import time
import random
K_CLUSTER = 10

def get_input_data(filename):
    input_file = open(filename, 'r')
    gene_ids = list()

    for i,line in enumerate(input_file):
        
        sp = line.strip().split('\t')
        data =[float(value) for value in sp]
        #gene_ids.append((i,)+tuple(data))
        gene_ids.append([i] + data)
    # 자료형, [index, v0, v1, ..., v12]
    return gene_ids

# 초기에는 random한 10개의 medoid 선택
#done
def initialize_medoids(data):
    init_medoids =list()        
    init_medoids = random.sample(data,10)
    return init_medoids

#done
def calculate_euclidian_distance(dot1,dot2):
    # 0번째는 index 이므로 euclidian distance 계산에 포함 시키지 않음
    squared_distance = sum((dot1[i+1] - dot2[i+1]) ** 2 for i in range(12))
    distance = math.sqrt(squared_distance)
    return round(distance,3)

def calculate_total_cost_for_non_medoid(p, p_medoid, _490_matrix):

    # p와 p의 index_medoid와의 거리
    total_cost = calculate_euclidian_distance(p, p_medoid)

    for point2 in _490_matrix:
        total_cost += calculate_euclidian_distance(p,point2)


    return total_cost

def calculate_total_cost_for_medoid(medoid, _490_matrix):
    total_cost = 0

    for point in _490_matrix:

        total_cost +=(calculate_euclidian_distance(medoid, point))


    return total_cost

# randomly selected 된 medoids와 가까운거리의 points  할당
#done
def assign_clusters(medoids, data):
    clusters = {tuple(medoid): [] for medoid in medoids}
    
    for point in data:
        if point not in medoids:  # medoids 들은 거리 계산에서 제외
            min_distance = float('inf')
            closest_medoid = None
            # medoids 10개의 후보군 중에서, (point = medoid가 아닌 값 전체)

            # medoids가 아닌 data point들 각각은 10개의 medoids들과 거리가 계산된다.
            for medoid in medoids:
                d = calculate_euclidian_distance(point, medoid)
                #거리가 가장 최소인 medoid가 있는 cluster에 들어감
                if d <= min_distance:
                    min_distance = d
                    closest_medoid = tuple(medoid)
            # closest_medoid를 key값으로 사용하는 dictionary형에 들어가게 됨.
            clusters[closest_medoid].append(point)
    
    return clusters


def nearest_medoids(medoids,point): 
    min_distance = float('inf')
    
    for medoid in medoids:
        

        d= calculate_euclidian_distance(medoid,point)
        
        if d < min_distance:
            nearest_medoid = medoid
            min_distance = d
    
    index = nearest_medoid[0]
          
    return index


# point 별로 가장 가까운 medoid를 표현하기위해 medoids도 전달
# sorted 에서 non_medoids_list에 새로운 열 2개를 추가한다.
def generate_sorted_non_medoids_list(medoids, non_medoids_list):
    non_medoids_list_before_sorting =list()
    sorted_list = list()

    for point in non_medoids_list:
        
        add_list = list(point)

        add_list.append(calculate_euclidian_distance(medoids[0], point))
        add_list.append(nearest_medoids(medoids,point))


        non_medoids_list_before_sorting.append(add_list)
    
    sorted_list = sorted(non_medoids_list_before_sorting, key = lambda x:x[13], reverse=False )

    return sorted_list

def medoids_swap(medoids_list, _490_points_matrix):
    changed_490_matrix =list()
    check = 0

    for p in _490_points_matrix:
        #p의 total_cost와 p의 index medoid의 total_cost 필요
        for medoid in medoids_list:
         if p[14] == medoid[0]:
             p_index_medoid = medoid
            
        p_total_cost = calculate_total_cost_for_non_medoid(p, p_index_medoid,_490_points_matrix)
        p_index_meoid_total_cost = calculate_total_cost_for_medoid(p_index_medoid, _490_points_matrix)

        # non_medoid_total_cost가 현재 medoid_total_cost 보다 작음 발생
        if p_total_cost < p_index_meoid_total_cost:

            # medoids_list에서 p_index_medoid 빼고, p를 medoids_list로 추가
            # _490_points_matrix에서 p 빼버리고 p_index_medoid 추가
            for i in range(len(_490_points_matrix)):
                _490_points_matrix[i] = _490_points_matrix[i][:13]

            medoids_list.remove(p_index_medoid)
            medoids_list.append(p[:13])
            _490_points_matrix.remove(p[:13])
            _490_points_matrix.append(p_index_medoid)
            changed_490_matrix = _490_points_matrix
            return check, changed_490_matrix
        
        
    # 모든 points와 medoids들간에 변경이 일어나지 않았으면
    check =1



    return check , changed_490_matrix


def generate_clusters(total_points_data_list):
    final_cluster =dict()
    gene_id =list()

    medoids_list = initialize_medoids(total_points_data_list)
    non_medoids_list =total_points_data_list

    for row in medoids_list:
        if row in non_medoids_list:
            non_medoids_list.remove(row)    

     # [index, v1, ... v12, distance, nearest_medoid]
    sorted_non_medoids_matrix = generate_sorted_non_medoids_list(medoids_list, non_medoids_list)
    
    while True:
        #swap 진행
        check, new_490_matrix = medoids_swap(medoids_list,sorted_non_medoids_matrix)
        #다시 sorting
        sorted_non_medoids_matrix = generate_sorted_non_medoids_list(medoids_list,new_490_matrix)


        if not check == 0:
            break

    #new_medoids = k_medoids_algorithm(clusters)
    #변경된 medoids로 cluster 최종할당
    new_clusters = assign_clusters(medoids_list,total_points_data_list)
    

    #index만 분리
    for dic_k, dic_v in new_clusters.items():
        for value in dic_v:
            
            gene_id.append(value[0])
        
        final_cluster[dic_k[0]] = set(gene_id)
        gene_id.clear()

    return final_cluster

def output_to_file(result,filename):
    file = open(filename, 'w')

    for dic_k,dic_v in result.items():
        s = str(len(dic_v)+1) + ":" + str(dic_k) + ", " + ", ".join(map(str, dic_v)) + "\n"
        file.write(s)

    file.close()

def main():
    input_filename = 'assignment4_input.txt'
    output_filename = 'assignment4_output.txt'
    data_points = get_input_data(input_filename)
    #k_medoids are 10 lists randomly selected

    # clusters list and their size. (dic)
    start_time = time.time()
    clusters=generate_clusters(data_points)
    end_time = time.time()
    elapsed_time = end_time-start_time
    output_to_file(clusters,output_filename)
    print(elapsed_time)
    

if __name__ == '__main__':
    main()