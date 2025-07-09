from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# Convert a PDF file to a list of images (one image per page)
def pdf_to_images(pdf_path):
    """
    Convert a PDF file to a list of images.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of PIL Image objects
    """
    try:
        # Convert PDF to images (one per page)
        images = convert_from_path(pdf_path)
        return images
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        raise

def extract_text_from_image(image_path_or_object):
    """
    Extract text from an image using OCR.
    
    Args:
        image_path_or_object: Either a path to an image file or a PIL Image object
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # If input is a string (path), open the image
        if isinstance(image_path_or_object, str):
            image = Image.open(image_path_or_object)
        else:
            image = image_path_or_object
            
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        raise

def ocr_from_pdf(pdf_path):
    """
    Extract text from a PDF file by converting it to images and running OCR on each image.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Combined text from all pages of the PDF
    """
    try:
        # Convert PDF to images
        images = pdf_to_images(pdf_path)
        
        # Process each image and extract text
        full_text = ""
        for image in images:
            extracted_text = extract_text_from_image(image)
            full_text += extracted_text + "\n"
        
        return full_text
    except Exception as e:
        print(f"Error processing PDF for OCR: {str(e)}")
        raise
