
import random
import math

def initialize_medoids(data):
    init_medoids =list()        
    init_medoids = random.sample(data,10)
    return init_medoids

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
                if d < min_distance:
                    min_distance = d
                    closest_medoid = tuple(medoid)
            # closest_medoid를 key값으로 사용하는 dictionary형에 들어가게 됨.
            clusters[closest_medoid].append(point)
    
    return clusters

def calculate_euclidian_distance(dot1,dot2):
    # 0번째는 index 이므로 euclidian distance 계산에 포함 시키지 않음
    squared_distance = sum((dot1[i+1] - dot2[i+1]) ** 2 for i in range(12))
    distance = math.sqrt(squared_distance)
    return round(distance,3)

def generate_clusters(total_points_data_list):
    final_cluster =dict()
    gene_id =list()

    medoids_list = initialize_medoids(total_points_data_list)
    non_medoids_list = total_points_data_list
    new_clusters = assign_clusters(medoids_list,total_points_data_list)

    for dic_k, dic_v in new_clusters.items():
        for value in dic_v:
            
            gene_id.append(value[0])
        
        final_cluster[dic_k[0]] = set(gene_id)
        gene_id.clear()

    return final_cluster

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

def output_to_file(result,filename):
    file = open(filename, 'w')

    for dic_k,dic_v in result.items():
        s = str(len(dic_v)) + ":" + str(dic_k) + ", " + ", ".join(map(str, dic_v)) + "\n"
        file.write(s)

    file.close()

def main():
    input_filename = 'assignment4_input.txt'
    output_filename = 'assignment4_output.txt'
    data_points = get_input_data(input_filename)
    clusters = generate_clusters(data_points)
    output_to_file(clusters,output_filename)



if __name__ == '__main__':
    main()