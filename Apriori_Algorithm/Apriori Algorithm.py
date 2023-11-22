"""
홍한울 2019253022
"""

from math import ceil
from itertools import combinations

MIN_SUPPORT = 0.035

# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A dictionary of transactions and a set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    for line in input_file:
        splitted = line.split()
        trans_id = splitted[0]
        trans_items = splitted[1:]
        transactions[trans_id] = trans_items
        itemset.update(trans_items)
    return transactions, itemset
# make empty dictionary in transactions
# split text to trans_id and trans_items 
# each transactions are classified with trans_id

# This function calculates support of the itemset from transactions
# param transactions: All transactions in a dictionary
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def support(transactions, itemset):
    support_count = 0
    """
    done
    """
    for trans_item in transactions.values():
        if itemset.issubset(set(trans_item)):
            support_count+=1
    return support_count



# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
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


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
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


# This function generates candidate itemsets of size (itemset_size) by selective joining and apriori pruning
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: candidate itemsets formed by selective joining and apriori pruning
# when this method get stared, size 1,2 exist
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets


# This function generates a table of itemsets with all frequent items from transactions based on a given minimum support
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_sup: The minimum support to find frequent itemsets
# return: The table of all frequent itemsets of different sizes
def generate_all_frequent_itemsets(transactions, items, min_sup): # min_sup == 8

    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = list()
    frequent_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()
    """""
    done
    """""
    #first 
    for item in items:
        itemset =frozenset([item])
        itemset_support = support(transactions,itemset)
        # if item's support bigger than min_sup(8)
        if itemset_support >= min_sup:
            frequent_itemsets[itemset_size].append(itemset)
            
    

    # Frequent itemsets of greater size
    itemset_size += 1

    # stop loop when [size -1] itemsets dosent exist
    # bigger size fre_qrequent_itemsets is not 'real frequent' yet
    while frequent_itemsets[itemset_size - 1]: #size1 ....>
        frequent_itemsets[itemset_size] = list() #size2 ....>
        # candidate_itemsets : 
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size)
        pruned_itemset = set()
        """
        done
        """
        for itemset in candidate_itemsets:

         itemset_support = support(transactions, itemset)
         if itemset_support >= min_sup:
            pruned_itemset.add(itemset)

        frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    for itemset_size in frequent_itemsets_table:
    
        # Do not print frequent itemsets of size 0 or 1
        if itemset_size == 0:
            continue
        if itemset_size == 1:
            continue
        
        # Print frequent itemsets of size 2 or larger 
        for freq_itemset in frequent_itemsets_table[itemset_size]:
            support_percent = (support(transactions, freq_itemset) / len(transactions)) * 100
            file.write('{0} {1:.2f}% support\n'.format(freq_itemset, support_percent))
    file.close()


# The main function
def main():
    input_filename = '/Users/honghan-ul/Documents/datamining/assignment1_input.txt'
    output_filename = '/Users/honghan-ul/Documents/datamining/assignment1_output.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_sup = ceil(MIN_SUPPORT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_sup)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)



if __name__ == '__main__':
    main()