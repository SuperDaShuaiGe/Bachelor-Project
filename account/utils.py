from docx import Document
import PyPDF2
from openai import OpenAI

def read_docx(file_path):
    # Open a .docx file using the python-docx library and extract all text
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)  # Append each paragraph's text to the full_text list
    return '\n'.join(full_text)  # Join all paragraphs with newline characters

def read_pdf(file_path):
    # open pdf files
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = []
        # go over each pages
        for page in reader.pages:
            full_text.append(page.extract_text())  # Extract the text of each page and add it to a list
    return '\n'.join(full_text)  # Concatenate the text of all pages, separated by line breaks

def read_cpp_with_newlines(file_path):
    # open c++ files and read contents
    with open(file_path, 'r', encoding='utf-8') as file:
        content_lines = file.readlines()  # Read all lines, preserving the newline character at the end of each line

    # Concatenate all the lines and make sure there is a line break at the end of each line
    content = ''.join(line for line in content_lines)
    return content

def get_response(prompt, temperature=0.5, max_tokens=2048):
    # Function to generate text completions using the OpenAI GPT-3.5 API
    client = OpenAI(
        # Initialization with an API key (for access to OpenAI's services)
        api_key='',
    )
    completion = client.chat.completions.create(
        model="gpt-4o-2024-05-13",  # Specify the model used for the completion
        temperature=0,  # Set temperature to 0 for deterministic outputs
        top_p=0,  # Control the diversity of generated responses
        messages=[{"role": "user", "content": f"{prompt}"}]  # Input prompt as a user message
    )
    return completion.choices[0].message.content  # Extract and return the content of the response
