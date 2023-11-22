""""
2019253022_홍한울
"""
import math
import heapq
import time
K_CLUSTER = 10

def get_input_data(filename):
    input_file = open(filename, 'r')
    gene_ids = list()

    for i,line in enumerate(input_file):
        
        sp = line.strip().split('\t')
        data =[float(value) for value in sp]
        gene_ids.append((i,)+tuple(data))
    # 자료형, (index, v0, v1, ..., v12) tuple들의 list로 구성
    return gene_ids


# 수정 : 총 비용중 가장 작은 값 10개를 medoid 설정
def initialize_medoids(data):
    #medoids = list
    distance_result = list()
    medoids =list()        
    for candidate in data:
        candidate_distance = round(sum(calculate_euclidian_distance(candidate, p) for p in data),3)
        distance_result.append(candidate_distance)
   
   # 각 Point의 distance 중 하위 10개 선별
    smallest_10 = heapq.nsmallest(10,enumerate(distance_result), key =lambda x: x[1])
    # data에서 smallest_10의 index를 이용하여 초기 medoids선별
    medoids = [data[idx] for idx, _ in smallest_10]

    return medoids

def calculate_euclidian_distance(dot1,dot2):
    # 0번째는 index 이므로 euclidian distance 계산에 포함 시키지 않음
    squared_distance = sum((dot1[i+1] - dot2[i+1]) ** 2 for i in range(len(dot1)-1))
    distance = math.sqrt(squared_distance)
    return round(distance,3)
# 전체 non-medoids points들은 10개의 medoids들과 거리가 계산된후, 가장 가까운 클러스터에 들어간다.


def assign_clusters(data, medoids):
    clusters = {medoid: [] for medoid in medoids}
    
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
                    closest_medoid = medoid
            # closest_medoid를 key값으로 사용하는 dictionary형에 들어가게 됨.
            clusters[closest_medoid].append(point)
    
    return clusters

def update_medoids(clusters):
    new_medoids = []
    # key: medoid value : points(in the cluster without medoid)
    for medoid, points in clusters.items():
        new_medoid = medoid
        medoid_distance = sum(calculate_euclidian_distance(medoid, p) for p in points)
        medoid_distance = round(medoid_distance,3)
        #현재 points는 cluster로 묶여있는 data이다. (전체가 아님) 그리고 현재 medoide도 들어있지 않아.
        for point in points:
            total_distance = sum(calculate_euclidian_distance(point, p) for p in points)
            total_distance += calculate_euclidian_distance(point,medoid)
            total_distance=round(total_distance,3)
            # 조건이 만족한 경우는 현재 medoid보다 더 좋은 대안이 있다는 사실.

            if total_distance < medoid_distance:
                medoid_distance = total_distance
                new_medoid = point
        new_medoids.append(new_medoid)
    return new_medoids


def generate_clusters(total_points_data):
    final_cluster =dict()
    gene_id =list()
    medoids = initialize_medoids(total_points_data)
    while True:
        # medoids에 대하여 가까운 point를 할당
        clusters = assign_clusters(total_points_data, medoids)
    
        #medoid들의 변화
        new_medoids = update_medoids(clusters)
        
        # 중심점이 더 이상 변하지 않으면 종료
        if set(medoid[0:] for medoid in medoids) == set(new_medoids[0:] for new_medoids in new_medoids):
            break
        
        medoids = new_medoids
    
    for dic_k, dic_v in clusters.items():
        for value in dic_v:
            
            gene_id.append(value[0])
        
        final_cluster[dic_k[0]] = set(gene_id)
        gene_id.clear()

    return final_cluster


def output_to_file(result,filename):
    file = open(filename, 'w')

    for dic_k,dic_v in result.items():
        s=str(len(dic_v))+":"+ str(dic_v) + "\n"
        file.write(s)

    file.close()


# The main function
def main():
    input_filename = '/Users/honghan-ul/Documents/datamining/K-midoids_Algorithm/input_data.txt'
    output_filename = '/Users/honghan-ul/Documents/datamining/K-midoids_Algorithm/result1.txt'
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