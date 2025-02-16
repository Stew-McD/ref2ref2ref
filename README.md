# ref2ref2ref

Find citations recursively from DOIs and CrossRef.

## Table of Contents

- [ref2ref2ref](#ref2ref2ref)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Introduction

The `ref2ref2ref` project aims to automate the retrieval of citations from an initial list of DOIs. It fetches related citations recursively up to a specified depth using the CrossRef API.

My motivation for this project was to automate the process of finding related citations for a list of DOIs. I wanted to find the most relevant citations for a list of DOIs, and see how they branch out but I didn't want to do it manually. I also wanted to learn how to use the CrossRef API.

After collecting the list of relevant references, its then possible to scrape them from the web (direct, unpaywall, scihub, etc.) using my other repository [ref2pdf](<https://github.com/Stew-McD/ref2pdf>)

Next use case is then to take the downloaded pdfs and use them to train an existing FOSS machine learning model.
Maybe make a chatbot that can answer questions about the papers? Focussing on the ones in the first layer of the citation tree, then less so for the second layer, etc.

ATM. The output lists of dois are not tagged as to which layer they belong to. But each layer is saved in a separate file. So you can see which layer they belong to by looking at the file name.

After processing, you can take the list of DOIs and use them to download the pdfs, or throw the list into zotero for it to collect the metadata and maybe pdfs. 

Easy improvements:
- Connect the doi list output with Crossref again to fill in the metadata automatically.
- Output a proper bibtex file.

One cool thing to do would be to automate the production of a graph of the citation tree.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/Stew-McD/ref2ref2ref.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ref2ref2ref
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your `.bib` file containing the initial DOIs in the `data/input` directory. (make it if you have to :wink:)
2. Run the `main.py` script:

    ```bash
    python src/main.py
    ```

3. The list of related DOIs will be saved in the `data/output` directory.

## Configuration

The configuration file `config.py` in the `src` directory allows you to set the recursion depth and the input/output file names. See the comments in `config.py` for more details.

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## License

This project uses the Unlicense.

## Contact

- Stewart Charles McDowall
- Email: <s.c.mcdowall@cml.leidenuniv.nl>
- Github: [Stew-McD](https://github.com/Stew-McD)
- Company: CML, Leiden University
