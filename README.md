#######################################
#######################################
###############  Setup ################
#######################################
#######################################

First install Python 3 

Next install pipenv
    pip install pipenv

Then create Pipfile
    pipenv install

Next install spacy by the following commands
    pip install spacy
    python -m spacy download en_core_web_sm

Run using this
    pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr

The code is tested using sample.txt and is working properly.


#######################################
#######################################
#######  Working of the code  #########
#######################################
#######################################

This Python script is designed to censor sensitive information in text documents. Here's a breakdown of its functionality:

Argument Parsing: The script uses the argparse module to parse command-line arguments. Users can specify input files, output directory, special files for statistics, and flags to censor specific types of sensitive information like names, dates, phone numbers, and addresses.

Text Processing with SpaCy: The script utilizes the SpaCy library to perform natural language processing (NLP) tasks. It detects entities in the text such as names, dates, and geographical locations (addresses).

Censoring Sensitive Information: After detecting sensitive information, the script replaces the sensitive text with a sequence of black squares (█) of the same length to censor it.

File Processing: The script processes each input file, censors the sensitive information, and writes the censored text to corresponding output files in the specified output directory.

Statistics Generation: Optionally, the script can generate statistics about the sensitive information found in the input files. These statistics include the count of sensitive information types such as names, dates, addresses, and phone numbers.

Output: The script provides flexibility in output options. Users can specify a directory for storing censored files and/or a file for writing statistics. If no statistics file is specified, the script prints the statistics to the standard output.

Main Function: The main() function orchestrates the entire process by parsing arguments, setting up flags, loading SpaCy model, processing files, and generating statistics.

