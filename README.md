# Pabst
Try out dash for bank parser proj

Pabst is named after the legendary American beer 'Pabst Blue Ribbon', because PBR = Parsing Bank Records

PARSING WITH DOCKER
-------------------
- Assume that Docker is installed. 
    - Run `./setup_pabst` to set up the docker container. Warning, this will take a while.
    - Run `./pabst <FILENAME>` to run ocr parsing on a file. 


NOTES
---
- pdf to text(`exp_text_parser.py`) is currently better than ocr, used as default by `main_parser.py`
- Put all pdf files inside the `./parsing` directory to convert to csv. The csv files are output in `./data`

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

    activate [name-of-env] # switch to conda env
    python app.py   # Full main app
