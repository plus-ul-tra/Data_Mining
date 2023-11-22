"""
2019253022_홍한울
"""
# pruning non- closed itemsets : itemset에 대하여, tid-set을 구한다. tid set 간에 비교, 조건에 의해 merging,
from math import ceil

MIN_SUPPORT_PERCENT = 0.035

# This function reads a file under filenames and extracts all transactions and a set of distinct items
# param filename: The name of the input file
# return: A dictionary of transactions and set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transaction = dict()
    genes_set = set()

    for line in input_file:
        # add to dictionary from each line
        # dictionary keys: transaction ID(first column)
        # dictionary values: genes
        sp = line.strip().split('\t')
        transaction[sp[0]] = set(sp[1:])

        # add genes to genes_set
        genes_set.update(sp[1:])

    return transaction, genes_set

# pruning non-closed itemsets : itemset에 대하여, tid-set을 구한다. tid set 간에 비교, 조건에 의해 merging,
# This function computes the frequency of union set and prunes the non-closed branch for each itemset pair
# param frequent_itemsets: The table of frequent closed itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: merged itemsets which non-closed branches are removed
def apply_charm_algorithm(frequent_closed_itemsets, itemset_size):
    # 이전의 frequent_closed_itemset(support미달 까지 적용됨)
    copied = frequent_closed_itemsets[itemset_size - 1].copy()
    merged_itemsets = list()
    seen_itemsets = set()
    same_tid = list()
    same_set =list()

    for i, itemset1 in enumerate(copied):
        for j, itemset2 in enumerate(copied):
            if i >= j:
                continue
            new_itemset = itemset1[0] | itemset2[0]
            common_transactions = itemset1[1].intersection(itemset2[1])
            if len(new_itemset) == itemset_size and common_transactions and new_itemset not in same_set:
                merged_itemsets.append((new_itemset, common_transactions))
                seen_itemsets = new_itemset
                same_set.append( seen_itemsets )
                # merging 후 사용된 이전 size의 list에서 merging된 set의 부분집합들을 제거(재료로 사용되어 상위 size merging에 사용된 것들)
                frequent_closed_itemsets[itemset_size-1] = [tid for tid in frequent_closed_itemsets[itemset_size-1] if tid[1] != itemset2[1]]
             #same_set.append(seen_itemsets)
             #copied (itemset(frozenset), Tid)
             # 조건에 충족된 itemset들을 merged_itemsets에 추가
             #집합의 포함관계에 따라 삭제해주는 것이 필요(mergerd_itemset은 다음 단계에 필요, 이전 단계는 이미 현재 사이즈 생성에 사용되었으니, 수정해도 됨.)
             #transaction 값을 비교해서 같은게 존재하면 삭재하는 방향
        

    


    return merged_itemsets
# tid-set을 위해서 transaction의 id도 같이 함수에서 받아야하지 않나 -> list에서 (item, Tid)를 묶음
#support 미달인 것 자르기는  pruning 에서


# This function prunes merged_itemset if support is smaller than min_support
# param merged_itemsets: The list of merged itemset
# param min_support: The minimum support to find frequent itemsets
# return: frequent itemsets
def pruning_infrequenct_itemsets(merged_itemsets, min_support):
    pruned_itemsets = list()
    """
    FILL UP HERE!
    Prune the candidate itemset if its support is less than minimum support
    done
    """
    for tid_set in merged_itemsets:
        if len(tid_set[1]) >= min_support:
            pruned_itemsets.append(tid_set)

  
        #특정 itemset x에 대하여 전체 transaction에서 support가 min_sup 이하인것을 없앤다.
        

    return pruned_itemsets

#calculate itemset support
def support_and_tid (transaction, itemset):
    support_count = 0
    tid = set()
    for key, trans_item in transaction.items():
        if itemset.issubset(set(trans_item)):
            support_count += 1
            tid.add(key)
                    
    return support_count, tid

# This function generates a table of closed itemsets with all frequent items from transactions
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent closed itemsets of different sizes
def generate_all_frequent_closed_itemsets(transactions, items, min_support):
    frequent_closed_itemsets = dict()

    itemset_size = 0
    frequent_closed_itemsets[itemset_size] = list()
    frequent_closed_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_closed_itemsets[itemset_size] = list()

    """
    Find all frequent itemsets of size-1 and add them to the list
    done
    """
     #size 1 itemset set support를 위한 함수 사용
    for item in items :

        itemset = frozenset([item]) 
        tid_set = set()
        itemset_support,tid_set= support_and_tid(transactions, itemset)

        if itemset_support >= min_support :
             #support가 충족되고, 해당 item을 갖는 transactions 들의 Tid를 같이. itemset = frozenset, tid_set = set
             frequent_closed_itemsets[itemset_size].append((itemset,tid_set))
    
    # result : 85개의 size 1인 frequent_closed_itemsets[1]

    # Frequent itemsets of greater size
    itemset_size += 1
    # itemset_size = 2 <--

    while frequent_closed_itemsets[itemset_size - 1]: #--> 종료 조건

        # 1: size-2 ~ start
        frequent_closed_itemsets[itemset_size] = list()

        # get merged_itemsets by using charm algorithm
        merged_itemsets = apply_charm_algorithm(frequent_closed_itemsets, itemset_size)

        # if support is greater than min_support then add to pruned_itemsets
        pruned_itemsets = pruning_infrequenct_itemsets(merged_itemsets, min_support)

        # add pruned_itemsets to frequent_closed_itemsets
        frequent_closed_itemsets[itemset_size] = pruned_itemsets
        itemset_size += 1


    return frequent_closed_itemsets


# This function writes all frequent closed itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_closed_itemsets_table: The dictionary which contains all frequent closed itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_closed_itemsets_table, transactions):
    file = open(filename, 'w')

    for dic_k, dic_v in frequent_closed_itemsets_table.items():
        # skip if the size of sets is smaller than 2
        if dic_k < 2:
            continue
        for item in dic_v: 
                s = str(item[0])[10:-1] + " " + str(round(len(item[1]) / len(transactions) * 100, 2)) + " % support\n"
                file.write(s)
    file.close()

# The main function
def main():
    input_filename = '/Users/honghan-ul/Documents/datamining/Charm_Algoritm/assignment1_input.txt'
    output_filename = '/Users/honghan-ul/Documents/datamining/Charm_Algoritm/result.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_closed_itemsets_table = generate_all_frequent_closed_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_closed_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()