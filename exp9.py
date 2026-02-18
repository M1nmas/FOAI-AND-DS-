from itertools import combinations

# Function to calculate support
def get_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count / len(transactions)


# Apriori Algorithm
def apriori(transactions, min_support=0.5):
    # Step 1: Create initial itemset (L1)
    itemset = set()
    for transaction in transactions:
        for item in transaction:
            itemset.add(frozenset([item]))
    
    # L stores all levels of frequent itemsets
    L = []
    current_L = set()
    
    # Filter itemsets by support
    for item in itemset:
        if get_support(item, transactions) >= min_support:
            current_L.add(item)
    
    L.append(current_L)
    k = 2
    
    while True:
        # Generate candidate itemsets of size k
        candidates = set()
        current_list = list(current_L)
        
        for i in range(len(current_list)):
            for j in range(i + 1, len(current_list)):
                union_set = current_list[i] | current_list[j]
                if len(union_set) == k:
                    candidates.add(frozenset(union_set))
        
        # Check support for candidates
        next_L = set()
        for itemset in candidates:
            if get_support(itemset, transactions) >= min_support:
                next_L.add(itemset)
        
        if not next_L:
            break
        
        L.append(next_L)
        current_L = next_L
        k += 1
    
    # Flatten L into a single set
    all_frequent_itemsets = set()
    for level in L:
        all_frequent_itemsets |= level
    return all_frequent_itemsets


# MAIN: Example Usage
if __name__ == "__main__":
    # Sample dataset (transactions)
    transactions = [
        {"Milk", "Bread", "Eggs"},
        {"Bread", "Butter"},
        {"Milk", "Bread", "Butter", "Eggs"},
        {"Bread", "Eggs"},
        {"Milk", "Eggs"},
    ]
    
    min_support = 0.4
    result = apriori(transactions, min_support)
    
    print("Frequent Itemsets (Support >=", min_support, "):")
    for item in result:
        print(set(item))