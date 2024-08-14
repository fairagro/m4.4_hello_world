# Development Tooling
This folder contains the development tools to generate the data for this repository. To use the tooling install the python requirements first using
```bash
pip install -r requirements.txt
```
The script queries the wikidata SPARQL endpoint and writes a csv file into the repos root directory. The script can be executed by using
```bash
python make.py
```