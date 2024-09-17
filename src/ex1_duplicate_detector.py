from typing import List, Any
from collections import Counter

def detect_duplicates(input_list: List[Any]) -> List[Any]:
    """
    Detects all duplicate elements in a list.

    Args:
        input_list (List[Any]): The input list to check for duplicates.

    Returns:
        List[Any]: A list containing only the duplicated elements, in the order
                   they first appeared in the original list. If there are no
                   duplicates in the input list, this list will be empty.
    """

    # Firstly I'll count the number of occurences of each item in the input_list
    # using the Counter class. Then, to maintain the order of the elements, I'll
    # loop the input_list and check if the element has a count > 1 and if it was
    # not added already into the duplicates list. If that's the case, then we
    # add that new element in the list.
    duplicates = []
    count = Counter(input_list)

    # I decided to use a set for faster lookup of seen duplicates after testing with large lists.
    # The testing became MUCH faster with this method.
    seen_duplicates = set()
    
    # loop through the input_list to maintain the order of the elements, as mentioned above
    for item in input_list:
        if count[item] > 1 and item not in seen_duplicates:
            duplicates.append(item)
            seen_duplicates.add(item)
    
    return duplicates
