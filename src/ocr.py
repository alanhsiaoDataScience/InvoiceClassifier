'''
https://nanonets.com/blog/ocr-with-tesseract/
'''
import os
import json
import io
import tempfile
import uuid
import pandas as pd
import pytesseract
import cv2
from PIL import Image, PpmImagePlugin

# set this to your own tesseract file path
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
SAVE_FILE_PATH = '../datasets/ocr/'
PNGS_DIR_PATH = "../datasets/sample_images/"


def extract_invoices_multiple() -> list:
    """
    executes logic to extract raw text with ocr and get formatted questions from multiple invoices in directory
    """
    files = os.listdir(PNGS_DIR_PATH)
    index = 0
    while index < len(files):
        filename = files[index]
        if filename.endswith('.png'):
            img = cv2.imread(PNGS_DIR_PATH+filename)
            ocr_outputs = extract_raw_text(img)
            # write_txt_to_file(ocr_outputs, filename + '.txt')  # logging

        index += 1

    return ocr_outputs


def extract_invoice_single(contents) -> str:
    fd, temp_file_path = tempfile.mkstemp()
    with os.fdopen(fd, 'wb') as temp_file:
        temp_file.write(contents)  # Write bytes data to the temporary file

    img = cv2.imread(temp_file_path)
    ocr_outputs = extract_raw_text(img)
    os.remove(temp_file_path)

    # write_txt_to_file(ocr_outputs, str(uuid.uuid4()) + ".txt")  # logging

    return ocr_outputs


def write_txt_to_file(txt: str, file_name: str) -> None:
    """
    saves the ocr outputs to txt file in subdirectory for further processing
    """
    save_name = f'{SAVE_FILE_PATH}{file_name}'

    # Open the file in write mode
    with open(save_name, 'w') as file:
        # Write the string to the file
        file.write(txt)

    return None


def extract_raw_text(image: PpmImagePlugin.PpmImageFile) -> str:
    """
    runs ocr package to retrieve raw text from png file image
    """
    # txt = pytesseract.image_to_string(image).encode("utf-8")

    # Adding custom options
    # custom_config = r'--oem 3 --psm 6' # checkout tesseract 4.0 for custom options
    txt = pytesseract.image_to_string(image)

    # print(txt)  # debugging

    return txt


if __name__ == "__main__":
    extract_invoices_multiple()
