# bank-parser-dash
Try out dash for bank parser proj


NOTES
---
- need to clean OCR data a LOT
    - ensure all lines the same # of params
    - sometimes amount + account_number is somehow one field, leading to *extremely* large amounts, which display badly
    - had to manually edit CSV :(, difficult to automate??
    - can just remove bad data...
- pdf to text is much better


Dev
---
`/data` holds input csv data

Install:

For Windows, first install [miniconda](https://conda.io/miniconda.html) (follow setup to create env also) and then install dash with conda:

    conda install -c conda-forge pandas dash dash-html-components dash-core-components

Other:
    pip install -r requirements.txt
    pip install pandas

Running:

    conda env [name-of-env] # switch to conda env
    python app.py   # simple 'hello world' app
    python multi.py # multiple input, multiple output, interactive example
