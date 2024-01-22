from pylatex import Document, Section, Subsection, Command, Tabular
from pylatex.utils import italic, NoEscape
import datetime
import formatted_operations
import humancalculation

import random
#space = NoEscape(r'\phantom{3}')
#carryover = NoEscape(r"$_1$")

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')
            doc.append('Woah ')
 
        for i in range(5):
            num1 = random.randrange(0, 1000000000)
            num2 = random.randrange(0, 1000000000)
            formatted_operations.subtraction_table(num1,num2,doc)
        for i in range(5):
            num1 = random.randrange(0, 1000000000)
            num2 = random.randrange(0, 1000000000)
            formatted_operations.addition_table(num1,num2,doc)
        formatted_operations.addition_table(1000,3002,doc)
      
        formatted_operations.multiplication_table(329,103,doc)
        formatted_operations.multiplication_table(3232294,327682,doc)
        #formatted_operations.division_table(101,10,doc)
        formatted_operations.division_table(12405587,17,doc)
        formatted_operations.division_table(99947360,384,doc)
        formatted_operations.division_table(382749583,294,doc)
        formatted_operations.division_table(456,10,doc)
        #formatted_operations.division_table(90932,2,doc)
        formatted_operations.division_table(9174,94,doc)
        formatted_operations.division_table(221948348,11,doc)
        formatted_operations.division_table(121,11,doc)
        formatted_operations.division_table(90,10,doc)
        formatted_operations.division_table(4184729,9,doc)
        formatted_operations.division_table(4096,2,doc)
        humancalculation.returnOperations()
if __name__ == '__main__':
  
    # Document with `\maketitle` command activated
    doc = Document()
    doc.packages.append(Command('usepackage','cancel')) #use for subtraction
    doc.packages.append(Command('usepackage','amssymb'))

    doc.preamble.append(Command('title', 'Awesome Title'))
    doc.preamble.append(Command('author', 'Anonymous author'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    fill_document(doc)


    # Add stuff to the document
    with doc.create(Section('A second section')):
        doc.append('Some text.')
        doc.append("This is some text i am testing if it right aligns or centers or whatever")

    doc.generate_tex('Z_sampleoutput')
    doc.generate_pdf('Z_sampleoutput', clean_tex=False)

    tex = doc.dumps()  # The document as string in LaTeX syntax