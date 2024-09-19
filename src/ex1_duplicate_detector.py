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


def main():
    """
    Main function to demonstrate the usage of the detect_duplicates function.
    This function allows users to input a list of elements and displays the detected duplicates.
    
    Usage:
        python -m ex1.src.ex1_duplicate_detector
    
    The user will be prompted to enter elements. To finish input, the user should press Enter without typing anything.
    """
    print("Enter elements of the list (press Enter without input to finish):")
    input_list = []
    while True:
        element = input()
        if element == "":
            break
        input_list.append(element)
    
    print("\nInput list:", input_list)
    duplicates = detect_duplicates(input_list)
    print("Detected duplicates:", duplicates)

if __name__ == "__main__":
    main()
