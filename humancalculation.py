from inputparser import read_input 
import formatted_operations
from pylatex import Document, Section, Subsection, Command, Tabular
import sys
import os


def returnOperations(input,doc):
    '''Calls one of the four operations functions on the doc based on user input.  Throws errors if input not properly formatted
    Args:
        input: string of user input
        doc: document to add table to
    Returns
        none
    '''
    '*','+','-','/','x','÷'
    parsedInput = read_input(input)
    match parsedInput[0]:
        case '+':
            formatted_operations.addition_table(parsedInput[1],parsedInput[2],doc)
        case '-':
            formatted_operations.subtraction_table(parsedInput[1],parsedInput[2],doc)
        case '*':
            formatted_operations.multiplication_table(parsedInput[1],parsedInput[2],doc)
        case 'x':
            formatted_operations.multiplication_table(parsedInput[1],parsedInput[2],doc)
        case '/':
            formatted_operations.division_table(parsedInput[1],parsedInput[2],doc)
        case '÷':
            formatted_operations.division_table(parsedInput[1],parsedInput[2],doc)


if __name__ == '__main__':
    '''filepath = os.path.join('c:/your/full/path', 'filename')
    if not os.path.exists('c:/your/full/path'):
        os.makedirs('c:/your/full/path')
    f = open(filepath, "a")
    '''

    if len(sys.argv) != 2:
        raise Exception("Equation to calculate must be wrapped in string")
    input = sys.argv[1]
    doc = Document()
    doc.packages.append(Command('usepackage','cancel')) #use for subtraction
    doc.packages.append(Command('usepackage','amssymb'))
    returnOperations(input,doc)
    doc.generate_pdf('Z_sampleoutput', clean_tex=False)
