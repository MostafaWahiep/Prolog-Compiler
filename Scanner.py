import tkinter as tk
from enum import Enum
import re
import pandas
import graphviz as gv
from pandastable import Table
from utils import *
from classes import *


def find_token(text):
    Tokens = []
    text, comments = extract_comments(text)
    for comment in comments:
        Tokens.append(token(comment, token_type.Comment))
    #text, string_dict = extract_string_literals(text)
    text = spacify(text)

    line_list = text.split('\n')

    comment = ""
    string = ""

    for l in line_list:
        l = l.strip()
        tokens = [a for a in l.split(' ') if a != ' ' and a != '']
        ind = 0
        print(tokens)
        while ind < len(tokens):
            t = tokens[ind]
            # Check for comments
            if t == "%":
                Tokens.append(token(t, token_type.line_comment))  # %
                comment = ' '.join(x for x in tokens[ind + 1:])
                Tokens.append(token(comment, token_type.Comment))  # comment
                comment = ""
                break
            elif t[0] == "\"":
                j = ind + 1
                while j < len(tokens) and tokens[j][-1] != '\"':
                    j += 1
                string = ' '.join(tokens[ind:j + 1])
                Tokens.append(token(string, token_type.String))
                ind = j + 1
                continue

            # Check for reserved words
            if t in reserved_words:
                Tokens.append(token(t, reserved_words[t]))
            elif t in reserved_operators:
                Tokens.append(token(t, reserved_operators[t]))

            #check for variables and data values
            elif re.match(r'^[A-Z_][a-zA-Z0-9_]*$', t):
                Tokens.append(token(t, token_type.variable_name))
            elif re.match(r'^[0-9]+$', t):
                Tokens.append(token(t, token_type.Integer))
            elif re.match(r'^[0-9]+\.[0-9]+$', t):
                Tokens.append(token(t, token_type.Real))
            #elif re.match(r'^\".*\"$', t):
            #Tokens.append(token(string_dict[t[1:-1]], token_type.String))
            elif re.match(r'^\'.\'$', t):
                Tokens.append(token(t, token_type.Char))
            elif re.match(r'^[a-z][a-zA-Z0-9_]*$', t):
                Tokens.append(token(t, token_type.Name))
            elif re.match(r'^_$', t):
                Tokens.append(token(t, token_type.Anonymous))
            else:
                Tokens.append(token(t, token_type.Error))
            ind += 1

    return Tokens


root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=600)


def Scan():
    x1 = entry1.get('1.0', 'end-1c')
    tokens = find_token(x1)
    arr = [t.to_dict() for t in tokens]
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    df = pandas.DataFrame.from_records([t.to_dict() for t in tokens])
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()
    canvas1.update_idletasks()
    canvas1.config(scrollregion=canvas1.bbox('all'))


canvas1.pack(side='left', fill='both', expand=True)
scrollbar = tk.Scrollbar(root, command=canvas1.yview)
scrollbar.pack(side='right', fill='y')
canvas1.config(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas1)
canvas1.create_window((0, 0), window=frame, anchor='nw')

label1 = tk.Label(frame, text='Scanner Phase')
label1.config(font=('helvetica', 14))

label2 = tk.Label(frame, text='Source code:')
label2.config(font=('helvetica', 10))
entry1 = tk.Text(frame, width=100, height=30)

label1.pack()
label2.pack()
entry1.pack()
button1 = tk.Button(frame,
                    text='Scan',
                    command=Scan,
                    bg='brown',
                    fg='white',
                    font=('helvetica', 9, 'bold'))
button1.pack()

frame.update_idletasks()
canvas1.config(scrollregion=canvas1.bbox('all'))
root.mainloop()