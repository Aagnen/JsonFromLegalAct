import PyPDF2
import re


# ---------------------------------------- METHODS --------------------------------------------------#

def universal_split(text_string, regex_to_find, regex_to_leave_in_name, name):
    result_dict = {}
    current_key = None

    pattern = re.compile(f"({regex_to_find})")
    pattern_to_name = re.compile(regex_to_leave_in_name)

    text_split = re.split(pattern, text_string)
    for line in text_split:
        match = pattern.search(line)
        if match:
            match_in_key = pattern_to_name.search(match.group(0).strip())
            if match_in_key:
                current_key = f"{name}{match_in_key.group(0)}"
            else:
                current_key = f"{name}0"
            while current_key in result_dict:
                current_key = f"{current_key}*"
            result_dict[current_key] = line[len(match.group(0)):].strip()
        elif line.strip() != "":
            if current_key is None:
                current_key = f"{name}0"
                result_dict[current_key] = line
            else:
                result_dict[current_key] += line

    return result_dict