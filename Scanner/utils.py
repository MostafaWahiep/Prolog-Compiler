from enum import Enum
import re



def extract_string_literals(code_text):
    string_literals = re.findall(r'\"(.*?)\"', code_text)
    strings_dict = {}
    for i in range(len(string_literals)):
        strings_dict[string_literals[i]] = string_literals[i].replace(
            f' ', f'')
    print(string_literals)
    print(strings_dict)

    for i in string_literals:
        code_text = code_text.replace(f'{i}', f'{strings_dict[i]}')
    strings_dict = {value: key for key, value in strings_dict.items()}
    return code_text, strings_dict


def extract_comments(code_text):
    comments = re.findall(r'/\*(.*?)\*/', code_text)
    for i in comments:
        code_text = code_text.replace(f'{i}', f' ')
    return code_text, comments


def find_element_index(lst, element):
    try:
        index = lst.index(element)
    except ValueError:
        index = -1
    return index


def spacify(text):
    # The regular expression pattern matches any string that starts and ends with double quotes
    # and may contain escaped characters inside the quotes.
    matches = re.findall(
        r'/\*.*?\*/|\".*?\"|<=|>=|<>|<>|=|<|>|[^:]-|\/[^\*]|[^\*]\/', text)
    # Find all matches of the regular expression pattern in the text.
    for match in matches:
        text = text.replace(f'"{match}"', f' "{match}" ')

    lst = ["+", ":-", ".", "(", ")", ",", ";", "%"]
    for i in lst:
        text = text.replace(f'{i}', f' {i} ')
    return text