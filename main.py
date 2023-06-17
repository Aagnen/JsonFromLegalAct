# importing required modules
import PyPDF2
import re
import json
import Methods

# ----------------------------------------CONSTANTS --------------------------------------------------#

# FILENAME = '1_D20212351Lj'
# H_MAIN_TEXT = 11  # the height of main text, larger that footnotes -> so it will exclude them
# ART_LOOKOUT = r"Art\.\s*\d+[a-z]?\."
# UST_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[.]\s*"
# PP_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[)]\s*"
# KEEP_IN_NAME = r"\d{1,4}[a-z]{,3}"

# FILENAME = '2_D20221225'
# H_MAIN_TEXT = 9
# ART_LOOKOUT = r"§\s*\d+[a-z]?\.\s*"
# UST_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[.]\s*"
# PP_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[)]\s*"
# KEEP_IN_NAME = r"\d{1,4}[a-z]{,3}"

FILENAME = '3_D20221679'
H_MAIN_TEXT = 9
ART_LOOKOUT = r"§\s*\d+[a-z]?\.\s*"
UST_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[.]\s*"
PP_LOOKOUT = r"\n+\s*\d{1,4}[a-z]{,3}[)]\s*"
KEEP_IN_NAME = r"\d{1,4}[a-z]{,3}"



# ---------------------------------------- PREPARE FILE --------------------------------------------------#
# creating a pdf file object
pdfFileObj = open(f'PDForyginaly/{FILENAME}.pdf', 'rb')
print("Opened")

# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)
print("Read")


# ---------------------------------------- PDF READING--------------------------------------------------#

def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    h = font_size
    # if 50 < y < 720 and h > 11:
    #     parts.append(text)
    if h > H_MAIN_TEXT:
        parts.append(text)
    return parts


raw_text = ""
for page in pdfReader.pages:
    parts = []
    text = page.extract_text(visitor_text=visitor_body)
    text = "".join(parts)
    #print(f' {pdfReader.get_page_number(page)}', end=" ")
    raw_text = raw_text + "\n" + text

print('\nText extracted')


# ---------------------------------------- PROCESSING --------------------------------------------------#

dict_out = {}

dict_art = Methods.universal_split(raw_text, ART_LOOKOUT, KEEP_IN_NAME, "Art.")
dict_out = dict_art

for key in dict_art:
    content = dict_art[key]
    dict_ust = Methods.universal_split(content,  UST_LOOKOUT, KEEP_IN_NAME, "Ust.")
    for key_1 in dict_ust:
        content_1 = dict_ust[key_1]
        dict_pdp = Methods.universal_split(content_1, PP_LOOKOUT, KEEP_IN_NAME, "Pp.")
        dict_ust[key_1] = dict_pdp

    dict_out[key] = dict_ust

print('Text processed')

# ---------------------------------------- SAVE --------------------------------------------------#

with open(f"text/{FILENAME}.txt", "w", encoding='utf-8') as outfile:
    outfile.write(raw_text)

with open(f"Json/{FILENAME}.json", "w", encoding='utf-8') as outfile:
    json.dump(dict_out, outfile)

print('Files saved')

# closing the pdf file object
pdfFileObj.close()
