import argparse  # Module for parsing command-line arguments
import glob  # Module for finding pathnames matching a specified pattern
import os  # Module for interacting with the operating system
import sys  # Module for interacting with the Python interpreter
import spacy  # Module for natural language processing
import re  # Module for regular expressions

# Function to detect sensitive information in text using SpaCy
def detect_sensitive_information(text, nlp, flags):
    doc = nlp(text)
    sensitive_info = {'names': [], 'dates': [], 'addresses': [], 'phones': []}
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and 'names' in flags:
            sensitive_info['names'].append(ent.text)
        elif ent.label_ == 'DATE' and 'dates' in flags:
            sensitive_info['dates'].append(ent.text)
        elif ent.label_ == 'GPE' and 'addresses' in flags:
            sensitive_info['addresses'].append(ent.text)
    if 'phones' in flags:
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        sensitive_info['phones'] = re.findall(phone_pattern, text)
    return sensitive_info

# Function to censor sensitive information in text
def censor_text(text, sensitive_info, flags):
    censored_text = text
    if 'names' in flags:
        for info in sensitive_info['names']:
            censored_text = censored_text.replace(info, '█' * len(info))
    if 'dates' in flags:
        for info in sensitive_info['dates']:
            censored_text = censored_text.replace(info, '█' * len(info))
    if 'addresses' in flags:
        for info in sensitive_info['addresses']:
            censored_text = censored_text.replace(info, '█' * len(info))
    if 'phones' in flags:
        for info in sensitive_info['phones']:
            censored_text = re.sub(r'\b{}\b'.format(info), '█' * len(info), censored_text)
    return censored_text

# Function to process each file
def process_file(file_path, output_directory, nlp, flags):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sensitive_info = detect_sensitive_information(text, nlp, flags)
    censored_text = censor_text(text, sensitive_info, flags)

    output_file_path = os.path.join(output_directory, os.path.basename(file_path) + '.censored')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(censored_text)

    return sensitive_info, output_file_path

# Function to write statistics to a file
def write_statistics(stats_file, sensitive_info):
    with open(stats_file, 'w') as stats:
        stats.write("Sensitive Information Statistics:\n")
        for category, info_list in sensitive_info.items():
            stats.write("{}: {}\n".format(category.capitalize(), len(info_list)))

# Main function
def main():
    parser = argparse.ArgumentParser(description='Censor sensitive information in text documents.')
    parser.add_argument('--input', nargs='+', help='Glob pattern representing input files')
    parser.add_argument('--output', help='Directory to store censored files')
    parser.add_argument('--stats', help='File to write statistics or special files (stderr, stdout)')
    parser.add_argument('--names', action='store_true', help='Censor names')
    parser.add_argument('--dates', action='store_true', help='Censor dates')
    parser.add_argument('--phones', action='store_true', help='Censor phone numbers')
    parser.add_argument('--addresses', action='store_true', help='Censor addresses')

    args = parser.parse_args()

    flags = []
    if args.names:
        flags.append('names')
    if args.dates:
        flags.append('dates')
    if args.phones:
        flags.append('phones')
    if args.addresses:
        flags.append('addresses')

    nlp = spacy.load('en_core_web_sm')

    input_files = []
    for pattern in args.input:
        input_files.extend(glob.glob(pattern))

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    all_sensitive_info = {'names': [], 'dates': [], 'addresses': [], 'phones': []}
    for file_path in input_files:
        sensitive_info, censored_file_path = process_file(file_path, args.output, nlp, flags)
        for category, info_list in sensitive_info.items():
            all_sensitive_info[category].extend(info_list)

    if args.stats:
        write_statistics(args.stats, all_sensitive_info)
    else:
        # Print statistics to stdout if --stats flag is not provided
        sys.stdout.write("Sensitive Information Statistics:\n")
        for category, info_list in all_sensitive_info.items():
            sys.stdout.write("{}: {}\n".format(category.capitalize(), len(info_list)))

if __name__ == '__main__':
    main()
