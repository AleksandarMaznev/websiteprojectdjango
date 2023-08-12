from docx import Document


def extract_text_from_docx(docx_file):
    text = []
    with docx_file.open(mode='rb') as docx_content:
        doc = Document(docx_content)
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

    return text
