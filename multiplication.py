from addition import int_to_equal_arrays as ints_array
int_array = lambda x : ints_array(x,0)[0] #int array of 1 number

def calculate_partial_products(num1: int, num2: int):
    '''calculate_partial_products: Returns a list of partial products of num1 and num2, with num2 as multiplier. Zero places are skipped.
    
    Args:
        num1: positive integer, > num2
        num2: positive integer, < num1
    Returns:
        partial_product_list: a list of all of the partial products of num1 and num2, starting with least significant digit'''
    partial_product_list = []
    array2 = int_array(num2)

    for i in range(len(array2)-1,-1,-1): #going in reverse order
        if array2[i] != 0:
            partial_product_list.append(array2[i] * num1 *  (10**(len(array2)-i-1)))
    return partial_product_list

def calculate_multiplication_carryovers(num1: int, num2: int):
    '''Returns array of arrays of the carryovers above the multiplicand needed to complete the multiplication problem
    
    For the kth digit, multiplies the k+1 digits, adds their carryover digit, then takes the 10th place digit.  Array is size(len(num1)), shifted one to the left.
    If we ignore shifting to the left, I think it would be the kth digit being the multiplication of the kth digits of the multiplication.
    Will make it size len(num1) + 1 to reduce edge cases
    Args:
        num1: positive integer > num2
        num2: positive integer < num1
    Returns:
        carryover_array_array: array of arrays of carryover digits, 0 if no carryover needed'''
    
    carryover_array_array = []
    array1, array2 = int_array(num1), int_array(num2) #we don't want them equal size so we don't have to deal with extra zeroes
    for i in array2:
        current_carryover_array = [0]
        non_zeroes = False
        for x in enumerate(reversed(array1)):
            whole_number = i * x[1] + current_carryover_array[x[0]] #we only want the tens digit of this
            tens = int((whole_number - (whole_number % 10))/10)

            if tens != 0:
                non_zeroes = True #we only want to add this array if it has valuable information: not if all zeroes

            current_carryover_array.append(tens)
        
        if non_zeroes: carryover_array_array.append(list(reversed(current_carryover_array)))
    return carryover_array_array

def calculate_addition_carryovers(num1: int, num2: int):
    '''Returns array of carryovers from addition in multiplication: partial products are added and if kth digit >= 10, carryover.

    Generalization of make_carryover_array from addition.py: multiple numbers are added from calculate_partial_products
    Args:
        num1: positive int > num2
        num2: positive int < num1
    Returns:
        carryover_array: array of carryover digits from addition subproblem within multiplication
    '''

    partial_product_list = calculate_partial_products(num1,num2)
    reversed_partial_product_list = list(reversed(partial_product_list)) #reversing so we can access max length easily

    max_length_int_array = lambda x : ints_array(x,reversed_partial_product_list[0])[0] #we want every int array to be the max int length
    digit_reversed_partial_product_list = [list(reversed(max_length_int_array(partial_product))) for partial_product in reversed_partial_product_list]

    carryovers = [0]
    for i in range(len(digit_reversed_partial_product_list[0])):
        sum_no_carryover = 0
        for partial_product in digit_reversed_partial_product_list:
            sum_no_carryover += partial_product[i]
        whole_number = sum_no_carryover + carryovers[i]

        tens = int((whole_number - (whole_number % 10))/10) #everything except first digit of number, so 0 if <10
        carryovers.append(tens)
    return list(reversed(carryovers))

def multiplication_table_components(num1: int, num2: int):
    '''Returns all non-formatted components necessary to make a multiplication table.
    
    Returns digitized multipilcation carryovers, num1,num2,addition carryovers,partial products,answer
    Args:
        num1: positive int > num2
        num2: positive int < num1
    Returns:
        all_parts_list: array list containing the specified above -> have thigns of undetermined length in a list so I know what to parse'''
    
    partial_products = calculate_partial_products(num1,num2)
    max_partial = partial_products[len(partial_products)-1]
    partial_product_digits = [ints_array(partial_product, max_partial)[0] for partial_product in partial_products]

    multiplication_carryovers = calculate_multiplication_carryovers(num1,num2)
    addition_carryovers = calculate_addition_carryovers(num1,num2)
    array1,array2 = ints_array(num1,num2)
    return [multiplication_carryovers,array1,array2,addition_carryovers,partial_product_digits,int_array(num1*num2)]



if __name__ == '__main__':
    print("Unit Tests")
    cppt = lambda x,y : print(calculate_partial_products(x,y)) #calculate_partial_product test
    cppt(485,392)
    cppt(3875,29385)
    #cppt(982,109)
    #cppt(694,100)
    cact = lambda x,y: print(calculate_addition_carryovers(x,y)) #calculate_addition_carryovers test
    cact(485,392)
    cact(3875,29385)
    cmct = lambda x,y: print(calculate_multiplication_carryovers(x,y)) #calculate_multiplication_carryovers test
    #cmct(694,100)
    #cmct(342,17)
    #cmct(23948,2394810)
    mtct = lambda x,y: print(multiplication_table_components(x,y)) #multiplication_table_components test
    mtct(3875,29385)
    mtct(3485,39235)