from pathlib import Path
import random
import os

# Maximum depth for recursion
RECURSION_DEPTH = 4

# Name of the input file
INPUT_FILE_NAME = 'bibliography.bib'

# Define directories and file paths
DIR_CWD = Path.cwd()
DIR_ROOT = DIR_CWD
DIR_DATA = DIR_ROOT / 'data'
DIR_OUTPUT = DIR_DATA / 'output'
DIR_INPUT = DIR_DATA / 'input'
DIR_TMP = DIR_DATA / 'tmp'

# Create directories if they don't exist
DIRS = [DIR_DATA, DIR_OUTPUT, DIR_INPUT, DIR_TMP]
for DIR in DIRS: 
    DIR.mkdir(exist_ok=True)


# Check for input file at root, else use default in 'data/input'
FILE_BIB = DIR_ROOT / INPUT_FILE_NAME if (DIR_ROOT / INPUT_FILE_NAME).exists() else DIR_INPUT / INPUT_FILE_NAME

# Make the output file name dependent on the input file name
OUTPUT_FILE_NAME = f"{INPUT_FILE_NAME.split('.')[0]}_output.txt"
FILE_TXT_OUT = DIR_OUTPUT / OUTPUT_FILE_NAME

# Generate a random email or use one from environment variable
EMAIL_FROM_ENV = os.getenv('EMAIL_CROSSREF')
random_email = f"scmm+{random.randint(0, 1000000)}@pm.me"
EMAIL = EMAIL_FROM_ENV if EMAIL_FROM_ENV else random_email

# Set Environmental Variables for crossref user agent
os.environ["CR_API_AGENT"] =  f"polite user agent; including mailto:{EMAIL}"
os.environ["CR_API_MAILTO"] = EMAIL
