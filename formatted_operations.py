from pylatex import Document, Section, Subsection, Command, Tabular, HFill, LineBreak, escape_latex
from pylatex.utils import italic, NoEscape
import addition
import subtraction
import multiplication
import random

#formatting characters from pylatex library
space = NoEscape(r'\phantom{3}')
carryover = NoEscape(r"$_1$")
carryover_digit = lambda x: NoEscape(r'$_{'+str(x)+r'}$')
int_array = lambda x : addition.int_to_equal_arrays(x,0)[0] #int array of 1 number


def hide_prefix_zeroes(num_array):
    '''hide_prefix_zeroes: Given array of integer digits, formats all prefix zeroes to be latex spaces

    Args: 
        num_array: array of integers representing digits
    Returns
        num_array: modified to have prefix zeroes before first non-zero digit
    '''
    current_num = 0
    while num_array[current_num] == 0 and current_num < len(num_array) - 1:
        num_array[current_num] = space
        current_num += 1
    return num_array



def subtraction_table_inner(num1,num2,doc):
    '''Generates LaTeX table representing the subtraction of two numbers.
    
    Subtracts two numbers.  num1 > num2 requirement.  Will be wrapped in subtraction function to deal with negatives
    
    Args:
        num1: positive integer > num2
        num2: positive integer < num1
        doc: doc object the table is added to
    Returns:
        none -> generates LaTeX table
    '''
    repl_array, bool_array, array1,array2,ans_array = subtraction.subtraction_table_components(num1,num2)

    #format to add strikethroughs in first number when a cancellation is needed - list comprehension checking boolean cancellation array to add latex format
    formatted_array1 =  [NoEscape(r'\cancel{' + str(x[1]) + r'}') if bool_array[x[0]] else x[1] for x in enumerate(array1)]
    #format replacements above the first row superscripted
    formatted_replacement_array = [space] +  [NoEscape(r'$_{'+str(x)+r'}$') if x != 100 else space for x in repl_array]

    #format spaces and operator
    number1 = [space] + formatted_array1
    number2 = [NoEscape(r'-')] + hide_prefix_zeroes(array2)
    ans_array = [space] + hide_prefix_zeroes(ans_array)

    #generate table
    
    with doc.create(Tabular('c@{\,}'*len(ans_array))) as table:
        table.add_row(formatted_replacement_array)
        table.add_row(number1)
        table.add_row(number2)
        table.add_hline(2, len(ans_array))
        table.add_row(ans_array)

def subtraction_table(num1,num2,doc):
    '''Generates LaTeX table representing the subtraction of two numbers.
    
    Subtracts two numbers.  If num2 > num1, switches them and explains  
    
    Args:
        num1: positive integer 
        num2: positive integer 
        doc: doc object the table is added to
    Returns:
        none -> generates LaTeX table
    '''
    with doc.create(Subsection('Subtraction Table')):
        post_append = False
        if num2>num1:
            doc.append(NoEscape(r'\raggedright'))
            doc.append(str(num1) + ' - ' + str(num2) + ' = -('+str(num2) + ' - ' +  str(num1) + ')')
            doc.append(LineBreak())
            num1,num2=num2,num1
            post_append = True
        subtraction_table_inner(num1,num2,doc)
        if post_append:
            doc.append(LineBreak())
            doc.append(NoEscape(r'$\therefore  $'))
            doc.append(f'   {num2} - {num1} = -{num1-num2}')


def addition_table(num1,num2, doc):
    '''Generates LaTeX table representing the addition of two numbers.
        
    Args:
        num1: positive integer 
        num2: positive integer 
        doc: doc object the table is added to
    Returns:
        none -> generates LaTeX table
    '''
    #maybe fix first number as higher

    bool_carryover_array, number1, number2, result = addition.addition_table_components(num1,num2)
    number1 = [space] + number1
    number2 = [NoEscape(r'+')] + hide_prefix_zeroes(number2)
    carryover_array = [carryover if i else space for i in bool_carryover_array]

    with doc.create(Subsection('Addition Table')):
            with doc.create(Tabular('c@{\,}'*len(carryover_array))) as table:
                table.add_row(carryover_array)
                table.add_row(number1)
                table.add_row(number2)
                table.add_hline(1, len(result))
                table.add_row(hide_prefix_zeroes(result))

def multiplication_table(num1,num2, doc):
    '''Generates LaTeX table representing the multiplication of two numbers.
    
    Need to work on edge cases more.
    Args:
        num1: positive integer
        num2: positive integer
        doc: doc object the table is added to
    Returns:
        none -> generates LaTeX table
    '''
    multiplication_carryovers, array1,array2,addition_carryovers,partial_product_digits,answer = multiplication.multiplication_table_components(num1,num2)
    formatted_addition_carryovers =  [NoEscape(r'$_{'+str(x)+r'}$') if x != 0 else space for x in addition_carryovers]
    formatted_multiplication_carryovers = []
    for row in multiplication_carryovers:
        formatted_multiplication_carryovers.append([NoEscape(r'$_{'+str(x)+r'}$') if x != 0 else space for x in row])


    format_zeroes = lambda x: hide_prefix_zeroes([0]*(len(formatted_addition_carryovers)-len(x)) + x)
    with doc.create(Subsection('Multiplication Table')):
            with doc.create(Tabular('c@{\,}'*len(formatted_addition_carryovers))) as table:
                #table.add_row(carryover_array)
                for row in formatted_multiplication_carryovers:
                    table.add_row(format_zeroes(row))
                table.add_row(format_zeroes(array1))
                #doc.packages.append(Command('cline','3-4')) #use for subtraction

                table.add_row(format_zeroes(['x'] + hide_prefix_zeroes(array2)))
                table.add_hline(min([len(str(num1)),len(str(num2))]),len(formatted_addition_carryovers))
                table.add_row(formatted_addition_carryovers)
                for partial_product in partial_product_digits:
                    table.add_row(format_zeroes(partial_product))
                
                table.add_hline(1, len(formatted_addition_carryovers))
                table.add_row(hide_prefix_zeroes(format_zeroes(answer)))

def division_table_inner(num1,num2,doc,is_integer):
    '''Inner function for division_table to deal with potential of non-integer return
    Args:
        num1: positive integer divisible by num2
        num2: positive integer
        doc: doc object the table is added to
        is_integer: boolean, if false, decimal needs to be added
    Returns:
        none -> generates LaTeX table
    '''
    num1 = num1 if is_integer else num1*100 #dealing with potential non-integer return
    array1,array2 = int_array(num1),int_array(num2)
    answer_digits = int_array(int(num1/num2))  
    second_row = array2 + [NoEscape(r'$|'+str(array1[0])+r'$')] + array1[1:] 
    add_decimal = lambda x,is_int: x[:-2] + [NoEscape(r'.'+str(x[-2])+r'')] + [x[-1]] if not is_int else x
    format_zeroes = lambda x: hide_prefix_zeroes([0]*(len(second_row)-len(x)) + x)
    specify_zeroes = lambda x,y: hide_prefix_zeroes([0]*(len(second_row)-len(x) - y) + x + [space] * y) #left aligns by index
    
    first_row = format_zeroes(answer_digits)

    with doc.create(Subsection('Division Table')):
            with doc.create(Tabular('c@{\,}'*len(first_row))) as table:
                table.add_row(add_decimal(first_row,is_integer))
                table.add_hline(len(array2)+1,len(first_row))
                table.add_row(add_decimal(second_row,is_integer))

                digit = answer_digits[0]

                multiplied = int_array(digit * num2)
                current_index = len(multiplied) #i think i have the wrong index, the formatting is screwing it up

                digits_to_subtract = array1[0:len(multiplied)]
                int_digits = addition.array_to_int(digits_to_subtract)
                table.add_row(specify_zeroes([NoEscape(r'-')] + multiplied,len(array1)-len(digits_to_subtract)))
                table.add_hline(len(array2)+1,len(array2)+len(multiplied))
                if len(digits_to_subtract) == len(array1):
                    next_row = int_array(int_digits - digit*num2)
                    table.add_row(specify_zeroes(next_row,0))
                    return

                else:
                    next_row = int_array(int_digits - digit*num2) + [array1[current_index]]#next digit pulled from array1
                    table.add_row(specify_zeroes(next_row,len(array1)-len(digits_to_subtract)-1))

                current_index += 1
                
        
                for digit in enumerate(answer_digits[1:]): #the position of the digit added after subtraction determines the position, use enumerate
                    multiplied = int_array(digit[1] * num2)
                
                    format_index = len(first_row) - (current_index + len(array2))
                    table.add_row(specify_zeroes([NoEscape(r'-')] + multiplied,format_index))
                    temp_length = len(next_row)

                    if digit[0] != len(answer_digits) -2:
                        next_row = int_array(addition.array_to_int(next_row) - digit[1]*num2) + [array1[current_index]]#next digit pulled from array1
                        table.add_hline(len(first_row)- format_index - temp_length + 1,len(first_row)-format_index)

                        table.add_row(specify_zeroes(next_row,format_index - 1))
                    #get rid of conditional, only iterate over the list w/o first and last element
                    else: #on the last iteration we do it a little differently -> not pulling an additional digit
                        next_row = int_array(addition.array_to_int(next_row) - digit[1]*num2) 
                        table.add_hline(len(first_row)-format_index - temp_length + 1,len(first_row)-format_index)

                        table.add_row(specify_zeroes(next_row,format_index))

                    current_index += 1
                    
def division_table(num1,num2,doc):
    '''Generates LaTeX table representing the division of two numbers.  num1 has to be divisble by num2
    can wrap this in function that deals with non divisible later
    Args:
        num1: positive integer divisible by num2
        num2: positive integer
        doc: doc object the table is added to
    Returns:
        none -> generates LaTeX table
    '''
    isinteger = False;
    if num1 % num2 == 0:
        isinteger = True;
    division_table_inner(num1,num2,doc,isinteger)
                