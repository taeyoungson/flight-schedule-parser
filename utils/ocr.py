from PIL import Image
import pytesseract

# only for windows
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def image_to_string(img: Image.Image, lang: str = "", config: str = "-l eng+kor --oem 3", timeout: int = 60) -> str:
    return pytesseract.image_to_string(img, lang=lang, config=config, timeout=timeout)
