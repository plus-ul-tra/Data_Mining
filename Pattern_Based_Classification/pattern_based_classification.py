"""

"""
from time import time
from math import ceil
from itertools import combinations
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

def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets

def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    apriori_pruned_itemsets = set()
    """
    done
    """
    for itemset in selected_itemsets:
        is_frequent = True
        for subset in combinations(itemset, itemset_size-1):
            if frozenset(subset) not in frequent_itemsets[itemset_size -1]:
                is_frequent = False
                break
        if is_frequent:
            apriori_pruned_itemsets.add(itemset)
    return apriori_pruned_itemsets

def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = set()
    """
    done
    """
    # combination of [itemset_size-1] 
    for itemset1 in frequent_itemsets[itemset_size-1]:
        for itemset2 in frequent_itemsets[itemset_size-1]:
            if itemset1 == itemset2:
                continue
            """if itemset2 in frequent_itemsets[itemset_size-2]: """
            new_itemset = itemset1 | itemset2
            joined_itemsets.add(new_itemset)
    return joined_itemsets

def generate_all_frequent_itemsets(transactions, items): 
    # {gene, cancer set} : support
    result =[]
    frequent_itemsets = {}
    size_1_items = set()
    
    # size_1
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
                if item1 != item2:
                    union_itemset.append(item1.union(item2))
        
        for itemset in union_itemset:
            itemset_support = support(transactions,itemset)
            if itemset_support >= MIN_SUPPORT:
                new_items_dict[tuple(sorted(itemset))] = itemset_support
        if not new_items_dict:
            break
        k+=1
        frequent_itemsets.update(new_items_dict)
        candidate =[set(items) for items in new_items_dict]
    
    for itemset, sup in frequent_itemsets.items():

        for size in range(1,len(itemset)):

            for a in combinations(itemset, size):
                a_set = set(a)
                b_set = itemset - a_set

                if not b_set.isdisjoint({'ColonCancer','BreastCancer'}):
                    confidence = sup / support(a_set)

                    if confidence >= 0.6 :
                        result.append(a_set,b_set,support,confidence)


    return result

def calculate_confidence(transactions, itemset):
    colon = 0
    breast = 0
    num_of_patient = 0
    for patient in transactions.values():
        #해당 유전자 조합을 갖는 환자가 colon인지 breast인지
        if itemset.issubset(set(patient)):
            num_of_patient += 1
            if patient[100]=='ColonCancer':
                colon+= 1
            else:
                breast += 1
    col_confidence = colon/num_of_patient
    breast_confidence = breast/num_of_patient

    if col_confidence >= 0.6 or breast_confidence >= 0.6:
        return max(col_confidence,breast_confidence)
    else:
        return 0
def output(file_name, results):
    file = open(file_name,'w')
    for result in results:
        if len(result[0]) >= 2: 
            file.write(f"{{{', '.join(result[0])}}} - {{{', '.join(result[1])}}}: {result[2]*100:.2f}% support, {result[3]*100:.2f}% confidence \n")




def main():
    input_filename = 'data.txt'
    output_file ='re.txt'
    patients_gene_data, all_item_set = get_input_data(input_filename)
    #100patients
    min_sup = MIN_SUPPORT * len(patients_gene_data)

    results_rules = generate_all_frequent_itemsets(patients_gene_data, all_item_set)
    output(output_file,results_rules)

    #output_filename = 'assignment8_optput.txt'



if __name__ == '__main__':
    main()