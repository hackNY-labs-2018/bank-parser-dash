# -*- coding: utf-8 -*-
"""This file is the main point of entry
for all parsing. It will attempt text extraction
first, then fallback to OCR.
"""

# Built-in modules
import argparse
import sys
import os

# Custom Modules
import ocr_parser
import text_parser

csv_headers = ','.join(["transaction_date","posting_date","description","location","reference_number","account_number","amount","\n"])

def write_to_csv(csv_data, pdf_filename):
    output_filename = './data' + os.path.splitext(pdf_filename)[0] + '.csv'
    print("Writing CSV to", output_filename)
    try:
        file = open(output_filename, 'w')
        file.write(csv_headers)
        file.write(csv_data)
        print('Done extracting text, written to {0}'.format(output_filename))
    except:
        print("Error: unable to write CSV to", output_filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Need exactly one argument for filename.")
        sys.exit()
    FILENAME = sys.argv[1]

    print("Attempting text extraction.")

    csv_data = text_parser.extract_to_csv(FILENAME)

    if len(csv_data) == 0:
        print("Text extraction failed; attempting OCR parsing.")
        csv_data = ocr_parser.parse(FILENAME)

    print(csv_data)

    write_to_csv(csv_data, FILENAME)


