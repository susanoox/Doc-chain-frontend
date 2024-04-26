from docx import Document

def read_word_file(file_path):
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

# Example usage:
file_path = '/home/ubuntu/Doc-chain-frontend/Backup/sample.docx'  # Replace with the path to your Word file
word_text = read_word_file(file_path)
print(word_text)

# pip install python-docx
