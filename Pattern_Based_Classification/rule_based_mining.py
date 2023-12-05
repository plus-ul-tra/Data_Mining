"""
"""
import time
from itertools import combinations
import sys

MIN_SUPPORT =0.3
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    buffer_list =[]
    for line in input_file:
        splitted = line.split()
        trans_id = splitted[0]
        trans_items = splitted[1:]
        buffer_list =[]
        for i, gene in enumerate(trans_items[:100]) :
            buffer_list.append(str(i+1)+gene)
            
        buffer_list.append(trans_items[100])    

        transactions[trans_id] = buffer_list
        itemset.update(buffer_list)
    return transactions , itemset

def support(transactions, itemset):
    support_count = 0
    for trans_item in transactions.values():
        if itemset.issubset(set(trans_item)):
            support_count+=1
    item_support = support_count/len(transactions)
    return item_support

def generate_all_frequent_itemsets(transactions, items): 
    # {gene, cancer set} : support
    result =[]
    frequent_itemsets = {}
    size_1_items = set()
    
    # size_1_item_set
    for item in items:
        s = set([item])
        item_support = support(transactions, s)
        if item_support >= MIN_SUPPORT:
            size_1_items.add(item)
    candidate =[{item} for item in size_1_items]
    
    #size_2 ~ 
    k=2
    while candidate:
        new_items_dict ={}
        union_itemset =[]
        for item1 in candidate:
            for item2 in candidate:
                union_itemset = item1.union(item2)
                if len(union_itemset) == k:
                    itemset_support = support(transactions,union_itemset)
                    if itemset_support >= MIN_SUPPORT:
                        new_items_dict[tuple(sorted(union_itemset))] = itemset_support
        if not new_items_dict:
            break
        k+=1
        frequent_itemsets.update(new_items_dict)
        candidate =[set(items) for items in new_items_dict]
    
    # find_rules
    for itemset, sup in frequent_itemsets.items():
        item = set(itemset)
        for size in range(1,len(item)):

            for a in combinations(item, size):
                a_set = set(a)
                kind_of_cancer = item - a_set

                if not kind_of_cancer.isdisjoint({'ColonCancer','BreastCancer'}):
                    # A -> B == A_union_B_support / A_support
                    confidence = sup / support(transactions, a_set)

                    if confidence >= 0.6 and len(a_set)>=2:
                        result.append((a_set,kind_of_cancer,sup*100, round(confidence*100,3)))


    return result

def output(file_name, results):
    file = open(file_name,'w')
    for result in results:
            file.write(f"{{{', '.join(f'gene {item}' for item in result[0])}}} - : {{{', '.join(result[1])}}}: support : {result[2]}% , confidence : {result[3]}%  \n")

def main():
    input_filename = 'data.txt'
    output_file = 'output.txt'
    patients_gene_data, all_item_set = get_input_data(input_filename)
    #100patients
    min_sup = MIN_SUPPORT * len(patients_gene_data)
    start_time = time.time()
    results_rules = generate_all_frequent_itemsets(patients_gene_data, all_item_set)
    end_time = time.time()
    print("elapsed time : " + str(end_time-start_time))
    output(output_file,results_rules)

    #output_filename = 'assignment8_optput.txt'



if __name__ == '__main__':
    main()