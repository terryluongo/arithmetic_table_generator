import formatted_operations
import re

def read_input(input):
    '''
    Parses the user input to return the right calculation, throwing errors if pattern does not match
    Raises exceptions for:
        1. Numbers are not positive integers
        2. There are more than two numbers
        3. Unrecognized operation(s)
    '''
    regex_string = "[-+]^(?:[0-9]*[.])?[0-9]+|(?<=\(|\/|\*)[+-](?:[0-9]*[.])?[0-9]+|(?:[0-9]*[.])?[0-9]+|[-+*\/()]"
    potential_matches = re.findall(regex_string,input)
 
    parsed_numbers = []
    parsed_operators = []
    for match in potential_matches:
        try:
             float(match)
        except ValueError:
            if match in set(['*','+','-','/','x','÷']):
                parsed_operators.append(match)
            else:
                raise Exception("Invalid characters.  Input must be an equation containing only numbers and accepted operators")
        else:
            try:
                int(match)
            except ValueError:
                raise Exception("Arguments must be positive integers")
            else:
                parsed_numbers.append(int(match))
            #could have negative numbers and too many operators be solved the same way -> check for more than one minus sign
    if len(parsed_operators) != 1 or len(parsed_numbers) != 2:
        raise Exception("Invalid equation.  Equation must have two positive integers and one operator")

    parsed_input = parsed_operators + parsed_numbers
    
    print(parsed_input)
    return parsed_input

if __name__ == '__main__':
    read_input("-24.5 / -7")
    read_input("-21 17")
    read_input("Jeremy")
    read_input("21 + -2 + 3 Jeremy ")
    


