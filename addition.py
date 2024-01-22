def make_carryover_array(num1, num2):
    '''make_carryover_array: Returns a boolean array of if carryover is needed for the addition problem

    The kth index of the array is True if the k+1 sum of num1 and num2 digits is >= 10
    
    Args:
        num1: positive integer
        num2: positive integer
    Returns:
        carryover_array: the boolean array of carryover values
    '''

    list1, list2 = int_to_equal_arrays(num1,num2)
    #returns boolean array of size max(len(str(num1)),len(str(num2)))
    #index k true if k+1 sum > 10
    #first we need to convert both numbers into arrays of equal lenght - prefix zeros
    carryover_array = [False] * (len(list1) + 1)
    for i in range(len(list2)):
        carryover_array[len(list2)-i - 1] = (list1[len(list1)-i - 1] + list2[len(list2)-i - 1] + carryover_array[len(carryover_array)-i - 1] > 9)
    return carryover_array


def int_to_equal_arrays(num1: int, num2: int):
    '''int_to_equal_arrays: Returns a list of two arrays with the digits of num1 and num2, of equal length with prefix zeroes added to the smaller number
    
    Args:
        num1: positive integer
        num2: positive integer
    Returns:
        [list1, list2] - arrays of integer digits of equal length
    '''
    list1 = list(str(num1))
    list2 = list(str(num2))
    dif = len(list1) - len(list2)
    if dif > 0:
        list2 = [0] * dif + list2
    if dif < 0:
        list1 = [0] * -dif + list1
    list1 = [int(i) for i in list1]
    list2 = [int(i) for i in list2]
    return [list1, list2]

def array_to_int(digit_array: list):
    '''array_to_int: converts a number in digit array form back to an integer
    
    Args:
        digit_array: digits in base 10 array
    Returns:
        number: positive integer
    '''
    number = 0
    current_base = 10 ** (len(digit_array) - 1)
    for digit in digit_array:
        number += digit * current_base
        current_base /= 10
    return int(number)

def sum_in_array(num1: int, num2: int):
    '''sum_in_array: Returns a list of digits of the sum of num1 and num2, of fixed length with a prefix zero

    Args:
        num1: positive integer
        num2: positive integer
    Returns:
        sum: sum of num1 and num2 in an array of digits with a fixed length (prefix zero if no carryover)
    '''
    idk_length_ans = list(str(num1+num2))
    if len(idk_length_ans) == max(len(str(num1)),len(str(num2))):
        return [0] + idk_length_ans
    return list(str(num1+num2))


def addition_table_components(num1: int, num2: int):
    """addition_table_components: Returns an array of all components of addition table: formatted inputs and outputs with carryover boolean array
    
    Args:
        num1: positive integer
        num2: positive integer
    
    Returns: 
        all_parts_list: array of length 4 with the following:
            carryover array: a boolean array if a 1 needs to be added or not (if two digits have a carryover sum)
            formatted num1 and num2
            array_sum: formatted answer
    """
    carryover = make_carryover_array(num1,num2)
    num_return1, num_return2 = int_to_equal_arrays(num1,num2)
    array_sum = [int(i) for i in sum_in_array(num1,num2)]
    return([carryover, num_return1, num_return2, array_sum])


#testing
if __name__ == '__main__':
    print([[1,1,5],[0,0,1]] == int_to_equal_arrays(115,1))
    print(int_to_equal_arrays(11,13525))
    print("Carryover Tests")
    print(make_carryover_array(100,900))
    print("Conclusion of Carryover Tests")
    print("Full Tests")
    print(addition_table_components(299,5203))
    print(type(addition_table_components(299,5203)))
    print(array_to_int([3,4,2]))
    print(array_to_int([0,1,0]))
    print(array_to_int([1]))
