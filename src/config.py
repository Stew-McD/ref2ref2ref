from pathlib import Path
import random
import os

def load_config(input_file='bibliography.bib', recursion_depth=4):
    config = {}
    # Maximum depth for recursion
    config['RECURSION_DEPTH'] = recursion_depth

    # Define directories and file paths
    config['DIR_CWD'] = Path.cwd()
    config['DIR_ROOT'] = Path(__file__).parent.parent
    config['DIR_DATA'] = config['DIR_ROOT'] / 'data'
    config['DIR_OUTPUT'] = config['DIR_DATA'] / 'output'
    config['DIR_INPUT'] = config['DIR_DATA'] / 'input'
    config['DIR_TMP'] = config['DIR_DATA'] / 'tmp'

    # Create directories if they don't exist
    DIRS = [config['DIR_DATA'], config['DIR_OUTPUT'], config['DIR_INPUT'], config['DIR_TMP']]
    for DIR in DIRS:
        DIR.mkdir(exist_ok=True)

    # Define file names
    config['FILE_BIB'] = config['DIR_INPUT'] / input_file
    config['FILE_TXT_OUT'] = config['DIR_OUTPUT'] / f"{input_file.split('.')[0]}_output.txt"

    # Generate a random email or use the one from environment variable
    EMAIL_FROM_ENV = os.getenv('EMAIL_CROSSREF')
    random_email = f"scmm+{random.randint(0, 1000000)}@pm.me"
    config['EMAIL'] = EMAIL_FROM_ENV if EMAIL_FROM_ENV else random_email

    # Set Environmental Variables for crossref user agent
    os.environ["CR_API_AGENT"] =  f"polite user agent; including mailto:{config['EMAIL']}"
    os.environ["CR_API_MAILTO"] = config['EMAIL']
    
    return config