# importing required modules
import pypdf
import re
import json
import Methods

# ----------------------------------------CONSTANTS --------------------------------------------------#

H_MAIN_TEXT = 11  # the height of main text, larger that footnotes -> so it will exclude them

# ---------------------------------------- PREPARE FILE --------------------------------------------------#
# creating a pdf file object
FILENAME = '1_D20212351Lj'
pdfFileObj = open(f'PDForyginaly/{FILENAME}.pdf', 'rb')
print("Opened")

# creating a pdf reader object
pdfReader = pypdf.PdfReader(pdfFileObj)
print("Read")


# ---------------------------------------- PDF READING--------------------------------------------------#

def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    h = font_size
    # if 50 < y < 720 and h > 11:
    #     parts.append(text)
    if h > 11:
        parts.append(text)
    return parts


raw_text = ""
for page in pdfReader.pages:
    parts = []
    text = page.extract_text(visitor_text=visitor_body)
    text = "".join(parts)
    # print(f' {pdfReader.get_page_number(page)}', end=" ")
    raw_text = raw_text + "\n" + text

print('Text extracted')


# ---------------------------------------- PROCESSING --------------------------------------------------#


dict_out = Methods.split_all(raw_text)

print('Text processed')

# ---------------------------------------- SAVE --------------------------------------------------#

with open(f"text/{FILENAME}.txt", "w") as outfile:
    outfile.write(raw_text)

with open(f"Json/{FILENAME}.json", "w") as outfile:
    json.dump(dict_out, outfile)

print('Files saved')

# closing the pdf file object
pdfFileObj.close()
