'''
|===============================================================|
| File: main.py                                                 |
| Project: ref2ref2ref                                          |
| Repository: www.github.com/Stew-McD/ref2ref2ref               |
| Description: Find citations recursively from dois & crossref  |
|---------------------------------------------------------------|
| File Created: Saturday, 28th October 2023 8:15:56 pm          |
| Author: Stewart Charles McDowall                              |
| Email: s.c.mcdowall@cml.leidenuniv.nl                         |
| Github: Stew-McD                                              |
| Company: CML, Leiden University                               |
|---------------------------------------------------------------|
| Last Modified: Saturday, 28th October 2023 9:06:25 pm         |
| Modified By: Stewart Charles McDowall                         |
| Email: s.c.mcdowall@cml.leidenuniv.nl                         |
|---------------------------------------------------------------|
|License: The Unlicense                                         |
|===============================================================|
'''
# Import packages
import argparse
import crossref_commons.retrieval

from tqdm import tqdm  
from time import sleep
from pathlib import Path  

# Import functions from other files
from parsebib import bib2df
from config import load_config

# Load configurations



# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process bibliography.')
parser.add_argument('--input_file', type=str, default='bibliography.bib', help='Input bibliography file')
parser.add_argument('--recursion_depth', type=int, default=4, help='Recursion depth')
args = parser.parse_args()

# Override values from config.py
RECURSION_DEPTH = args.recursion_depth
FILE_BIB = DIR_INPUT / args.input_file
FILE_TXT_OUT = DIR_OUTPUT / f"{args.input_file.split('.')[0]}_output.txt"
df = bib2df(FILE_BIB)
if df.empty:
    print('No data found, check input file')
    exit()

df['doi'] = df['doi'].str.replace(r'\\_', '_', regex=True)
bib_dois = df['doi'].dropna().tolist()

def get_related_dois(bib_dois, i=0):
    """
    Retrieves DOIs related to the given list of DOIs.
    
    Parameters:
    - bib_dois (list): List of original DOIs.
    - i (int): Iteration index used for logging and filename suffix.
    
    Returns:
    - list: Extended list of unique DOIs including original and related DOIs.
    """
    
    bib_dois_all = bib_dois.copy()
    bib_dois_extended = bib_dois.copy()
    sleep_duration = 0.1  

    for j, bib_doi in enumerate(tqdm(bib_dois, desc=f'Iteration {i+1}')):
        sleep_duration = max(0, sleep_duration - 0.1*sleep_duration)  
        try:
            ref = crossref_commons.retrieval.get_publication_as_json(bib_doi)
            refs = [x['DOI'] for x in ref['reference'] if 'DOI' in x.keys() and x['DOI'] not in bib_dois_extended]
            refs_all = [x['DOI'] for x in ref['reference'] if 'DOI' in x.keys()]
            bib_dois_extended.extend(refs)
            bib_dois_all.extend(refs_all)
            sleep(sleep_duration)
        except Exception as e:
            if '503' in str(e):
                sleep_duration = min(10, sleep_duration + 0.1*sleep_duration)
                sleep(sleep_duration)
            pass
    
    print(f'\n Finished!')
    print(f'Length of doi list (inc. duplicates {len(bib_dois_all)}')
    print(f'Length of doi list (supposedly no duplicates {len(bib_dois_extended)}')
    bib_dois_ext = list(set(bib_dois_extended))
    print(f'Length of doi set (actually no duplicates) {len(bib_dois_ext)}')

    filename = Path(f"{DIR_OUTPUT / FILE_TXT_OUT.stem}_{i}{FILE_TXT_OUT.suffix}")
    with open(filename, 'w') as f:
        for item in bib_dois_ext:
            f.write("%s\n" % item)
    print(f'Wrote new doi list to {filename}\n')
    
    return bib_dois_ext

for i in range(RECURSION_DEPTH):
    print(f'{"="*80}\n')
    print(f'\t** Searching for references {"of references " * i}**')    
    print(f'{"-"*80}\n')
    print(f'\t Iteration {i+1}/{RECURSION_DEPTH}')
    print(f'\t Using {FILE_BIB.name} as input')
    print(f'\t Length of doi list {len(bib_dois)}')
    print(f'{"-"*80}\n')
    bib_dois = get_related_dois(bib_dois, i)
    
    print(f'{"="*80}\n')

if __name__ == '__main__':
    # Load configurations
    config = load_config(input_file='your_input.bib', recursion_depth=5)

    # Now use config dictionary for your operations
    print(config['RECURSION_DEPTH'])