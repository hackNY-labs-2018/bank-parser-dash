""" EXPERIMENTAL Text Parser parses text directly from a PDF using the "pdfquery" library
- WARNING: Does some crazy assumptions in attempt to correct comma placement
- Trades generalizability for accuracy in niche case
- Operates on the principle that the first two cells are always dates, highly accurate,
and that the location and transaction name is the source of inaccuracy
"""

import os
import re
import sys

import pdfquery

def extract_transactions(pdf):
    """Extracts a list of all transactions in CSV format from a PDF
    """
    pages_in_pdf = len(pdf.pq('LTPage'))
    line_height = 9.84 # TODO: how to find this apart from hardcoding?
    transactions = []

    for page in range(1, pages_in_pdf + 1):
        purchases_header = pdf.pq(
            'LTPage[pageid=\'%s\'] \
            LTTextLineHorizontal:contains("Purchases and Adjustments")' % page)
        if purchases_header.attr('x0') is None or purchases_header.attr('y0') is None:
            continue
        x = float(purchases_header.attr('x0'))
        y = float(purchases_header.attr('y0'))

        t = pdf.extract([
            ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
            ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
             (x - 100, y - line_height, x + 500, y))
            ])['transactions']
        while len(t) == 6:
            t = ','.join([process_text_cell(cell) for cell in t])
            transactions.append(t)
            y -= line_height
            t = pdf.extract([
                ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
                ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
                 (x - 100, y - line_height, x + 500, y))
                ])['transactions']
    normalize_length(transactions)
    return '\n'.join(transactions)

def normalize_length(transactions):
    ''' smart post processing (ensure all lines exactly = NORM_LENGTH)
    '''
    LOC_INDEX = 3 # location(state) starts on 4th column, so zero-index = 3
    NORM_LENGTH = 8 # set norm
    loc_set = set() # store all locations seen before, no repeats
    li = LOC_INDEX

    ''' normalize long lines '''
    for index, line in enumerate(transactions):
        arr = line.split(',')
        if len(arr) > NORM_LENGTH:
            arr[li-1:li+1] = [' '.join(arr[li-1:li+1])]
        loc_set.add(arr[li])
        transactions[index] = ','.join(arr)
    # these two for-loops cannot be combined b/c one must run in full before the other
    loc_sorted = sorted(loc_set, key=lambda x: len(x), reverse=True) # sort locations by length

    ''' normalize short lines '''
    for index, line in enumerate(transactions):
        arr = line.split(',')
        if len(arr) >= NORM_LENGTH:
            continue
        # attempt to match longest locations first
        for loc in loc_sorted:
            if len(loc) == 0:
                continue
            cell = arr[li-1]
            if not cell.endswith(loc):
                continue
            k = cell.rfind(loc)
            arr[li-1] = cell[:k] # split by reverse indexOf
            arr.insert(li, cell[k:])
            break # max one match
        while len(arr) < NORM_LENGTH:
            # last resort: pad
            arr.insert(li, '')
        transactions[index] = ','.join(arr)
    
    # compress loc, so 8-->7 columns
    for ind, line in enumerate(transactions):
        arr = line.split(',')
        arr[li:li+2] = [' '.join(arr[li:li+2])]
        transactions[ind] = ','.join(arr)

def process_text_cell(cell):
    """Helper function to process each text cell extracted from a pdf
    """
    # regex that looks for multiple contiguous whitespace occurences (eg. multiple spaces)
    regex = r"\s\s+"
    # replaces regex matches with comma delineation, also strips whitespace from both ends
    return re.sub(regex, ",", cell.text.strip())

def extract_text_if_valid(filename):
    """Parses text from a pdf if it is valid; otherwise,
    returns an empty string.
    """
    if not filename.endswith('.pdf'):
        print('Sorry, only PDF files are supported for text extraction.')
        return ""
    # prevent space normalization in order to separate different text blocks in each line
    pdf = pdfquery.PDFQuery(
        filename,
        normalize_spaces=False,
        resort=False)
    pdf.load()

    return extract_transactions(pdf)

def extract_to_csv(filename):
    """Parses text from a pdf and returns a csv
    file if valid. Returns True if operation succeeded,
    False otherwise.
    """
    csv_data = extract_text_if_valid(filename)
    if len(csv_data) == 0:
        print("Error: no bank data extracted from", filename)
        return ""
    return csv_data

if __name__ == '__main__':
    print('Run main_parser.py instead.')
    '''
    # ensure filename is provided
    if len(sys.argv) != 2:
        print("Need exactly one argument for filename.")
        sys.exit()
    FILENAME = sys.argv[1]
    print(extract_to_csv(FILENAME))
    '''
