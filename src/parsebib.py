import bibtexparser
import pandas as pd

# Define a function to parse the BibTeX file and create a DataFrame

def bib2df(FILE_BIB):
    if str(FILE_BIB).endswith('.bib'):    
        with open(FILE_BIB, 'r', encoding='utf-8') as bibfile:
            # Parse the BibTeX file
            parser = bibtexparser.bparser.BibTexParser()
            parser.ignore_nonstandard_types = False
            bib_database = bibtexparser.load(bibfile, parser=parser)
            
            # Create a DataFrame from the parsed BibTeX data
            data = []
            for entry in bib_database.entries:
                data.append(entry)
            df = pd.DataFrame(data)
            
            return df
    
    elif str(FILE_BIB).endswith('.csv'):
        df = pd.read_csv(FILE_BIB)
        return df
    
    elif str(FILE_BIB).endswith('.json'):
        df = pd.read_json(FILE_BIB)
        return df
    
    elif str(FILE_BIB).endswith('.txt'):
        df = pd.read_csv(FILE_BIB, header=None)
        return df
    
    else:
        print('File type not supported')
        return None