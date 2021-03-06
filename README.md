# Pabst
Pabst is named after the legendary American beer 'Pabst Blue Ribbon', because PBR = Parsing Bank Records

Notes:
---
- uses the [Dash framework](https://dash.plot.ly/)
- pdf to text(`exp_text_parser.py`) is currently better than ocr, used as default by `main_parser.py`
- Put all pdf files inside the `./parsing` directory to convert to csv. The csv files are output in `./data`

Dev
---
`/data` holds input csv data

Installing viz-only, without Docker
---

For Windows, first install [miniconda](https://conda.io/miniconda.html) (follow setup to create env also) and then install dash with conda:

    conda install -c conda-forge pandas dash dash-html-components dash-core-components

Other:

    pip install -r requirements.txt
    pip install pandas

Running:

    activate [name-of-env] # switch to conda env
    python app.py   # Full main app

Installing OCR deps, without Docker
---

Tips: use Python 3, make sure if you have 64-bit python, install 64-bit dependency versions. Similarly, 32-bit dep versions for 32-bit python.
```
source venv/bin/activate # Remember to activate your virtualenv
pip install -r requirements.txt
Install imagemagick and libimagemagickdev (differs by platform). Available via apt on Ubuntu
Install tesseract (see above.)
```

Installing via Docker
---

PARSING WITH DOCKER
-------------------
- Install Docker (and Virtualbox if applicable). May need to install Docker Legacy and Docker Toolbox for older machines.
- Run `./setup_pabst` to set up the docker container. Warning, this will take a while.
- Run `./pabst <FILENAME>` to run ocr parsing on a file. 

