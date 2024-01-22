from addition import int_to_equal_arrays as ints_array

#important: figure out if num1 > num2
#will define methods with the expectation that num1 > num2
#will test for negatives in the other file, have to figure out after casting as int - more of a formatting thing 
#wait not it might be relevant to the computations


def array_difference(num1: int, num2: int):
    '''array_difference: Returns array of n+1 size that is the digits of the difference between num1 and num2.
    n is the max of the length of num1 and num2
    
    Args:
        num1: positive integer
        num2: positive integer
    Returns:
        answer: the absolute value of the difference between num1 and num2, in array digit form with 1 prefix zero
    '''
    max_size = max(len(str(num1)),len(str(num2)))
    difference_array_no_padding = list(str(abs(num1-num2)))
    answer =  [0] * (max_size - len(difference_array_no_padding)) + difference_array_no_padding
    answer = [int(i) for i in answer]
    return answer



def make_cancellations(num1: int, num2: int):
    '''make_cancellations: Returns a list of two arrays: bool_cancel_array is where subtraction digit replacement was needed, replacement_array fills the superscripted digits.
    
    Returns a list of two arrays.  Replacement_array is composed of the numbers written superscripted above the first row when replacement is needed for subtraction.
    If the number is not needed, the kth index is a 100 as a placeholder
    The second one is bool_cancel_array, which is a boolean array for formatting, so the digits that don't subtract properly can be crossed out.
    Behaves so that the larger number is on top, which will be formatted that way later
    Args:
        num1: positive integer
        num2: positive integer
    Returns:
        answer: list of replacement_array and bool_cancel_array'''

    if (num1 - num2) < 0:
            temp = num1
            num1 = num2
            num2 = temp
    array1,array2 = ints_array(num1,num2)
    ans_array = array_difference(num1,num2)
    bool_cancel_array = [False] * len(array1)
    replacement_array = [100] * len(array1)

    for i in range(len(array1)):
        if ans_array[i] + array2[i] != array1[i]:
            bool_cancel_array[i] = True
            replacement_array[i] = ans_array[i] + array2[i]
    return [replacement_array, bool_cancel_array]


def subtraction_table_components(num1: int, num2: int):
    """subtraction_table_components: Returns an array of all components of subtraction table: formatted inputs and outputs with carryover boolean array and replacements
    
    Args:
        num1: positive integer
        num2: positive integer
    
    Returns: 
        all_parts_list: array of length 5 with the following:
            repl_array and bool_array: the cancellations and replacements for the subtraction
            formatted num1 and num2
            ans_array: formatted answer
    """
    #retuns all things needed for subtraction
    repl_array, bool_array = make_cancellations(num1,num2)
    array1,array2 = ints_array(num1,num2)
    ans_array = array_difference(num1,num2)
    return [repl_array, bool_array, array1,array2,ans_array]


#testing
if __name__ == '__main__':
    #Unit Tests
    print("Array_difference tests")
    print([0,2,8,1] == array_difference(300,19))
    print([0,1] == array_difference(1,0))
    print([0,1,1] == array_difference(19,30))
    print("Make_cancellations tests")
    print(make_cancellations(1000,999))
    print(make_cancellations(2,1))
