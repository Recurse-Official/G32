'''
USE AS FOLLOWS:

from pdf2text import extract_text_and_images_with_ocr

'''

from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import fitz  # PyMuPDF for image extraction

def extract_text_and_images_with_ocr(pdf_path):
    # Initialize reader for text and PyMuPDF for images
    pdf_reader = PdfReader(pdf_path)
    pdf_doc = fitz.open(pdf_path)
    combined_content = []

    for page_number, (pdf_page, fitz_page) in enumerate(zip(pdf_reader.pages, pdf_doc), start=1):
        print(f"Processing page {page_number}...")
        
        # Extract text content
        text_content = pdf_page.extract_text().strip() if pdf_page.extract_text() else ""

        # Extract images and apply OCR
        image_texts = []
        angle=fitz_page.rotation
        for img_index, img in enumerate(fitz_page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image = image.rotate(-angle, Image.NEAREST, expand = 1)
            if angle!=0: print(f'Page was rotated by {angle}°. [FIXED]')
            # image.show()
            
            # Apply OCR on the image
            ocr_text = pytesseract.image_to_string(image)
            image_texts.append(ocr_text)

        # Combine text content and OCR results
        combined_page_content = f"Page {page_number}:\n{text_content}\n" + "\n".join(image_texts)
        combined_content.append(combined_page_content)

    # Combine all pages
    return "\n\n".join(combined_content)


# Example usage
import io

pdf_path = "D:/Srikar/Desktop/Policy_Circular.pdf"
result = extract_text_and_images_with_ocr(pdf_path)

# Save to a file or print
with open("D:/Srikar/Desktop/Policy_Circular.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("Mixed-content extraction complete!")