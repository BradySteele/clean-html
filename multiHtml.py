from bs4 import BeautifulSoup
import json
import re
import os

def extract_headers_and_paragraphs(input_file, output_folder, file_count):
    with open(input_file, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    def clean_text(text):
        clean_text = text.replace('\u00a0', ' ')
        clean_text = clean_text.replace('\n', ' ')
        clean_text = clean_text.replace('\u2019', "'")
        clean_text = clean_text.replace('\u2018', "'")
        clean_text = clean_text.replace('\u201c', "'")
        clean_text = clean_text.replace('\u201d', "'")
        clean_text = clean_text.replace('\u00ae', '(R)')
        clean_text = clean_text.replace('\u00a9', '(c)')
        clean_text = clean_text.replace('\u2022', '*')
        clean_text = clean_text.replace('\u2013', '-')
        clean_text = clean_text.replace('\t\t', '  ')
        clean_text = re.sub(r'\\"', "'", clean_text)
        return clean_text.strip()

    # Extract headers and paragraphs
    headers_with_paragraphs = []
    allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    for tag in soup.find_all(allowed_tags):
        cleaned_header = clean_text(tag.get_text())

        paragraphs = []
        next_element = tag.find_next()
        while next_element and next_element.name != tag.name:
            if next_element.name == 'p':
                text = next_element.get_text()
                clean_paragraph = clean_text(text)
                if clean_paragraph.strip() != "":
                    paragraphs.append(clean_paragraph)
            next_element = next_element.find_next()

        if paragraphs:
            headers_with_paragraphs.append({
                "header": cleaned_header,
                "paragraphs": paragraphs
            })

    # Create a JSON file for each HTML file parsed
    output_file = os.path.join(output_folder, f"json{file_count}.json")
    with open(output_file, 'w') as output:
        json.dump(headers_with_paragraphs, output, indent=4)
        print(f"Headers and paragraphs saved to {output_file}")

# Path to the directory containing HTML files
html_directory = 'data'
output_directory = 'json_output'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

file_count = 0

# Iterate through all HTML files in the directory
for filename in os.listdir(html_directory):
    if filename.endswith('.html'):
        input_html = os.path.join(html_directory, filename)
        extract_headers_and_paragraphs(input_html, output_directory, file_count)
        file_count += 1
