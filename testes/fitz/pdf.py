import re
from pdfminer.high_level import extract_pages, extract_text

text = extract_text("conta-ma.pdf")

for i in range(1614, 1630, 1):
    print(text[i])
