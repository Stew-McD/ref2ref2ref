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

from pathlib import Path  
import crossref_commons.retrieval
from time import sleep
from parsebib import bib2df
from tqdm import tqdm  

from config import RECURSION_DEPTH, FILE_BIB, FILE_TXT_OUT, DIR_OUTPUT

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
