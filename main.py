import tkinter as tk
import pandas as pd
import pandastable as pt
from Scanner.Scanner import *
from Parser.parser import *
from nltk.tree import *


root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=600)
root.title('Prolog Parser')


def Scan():
    x1 = entry1.get('1.0', 'end-1c')
    tokens = find_tokens(x1)
    arr = [t.to_dict() for t in tokens]
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    df = pd.DataFrame.from_records([t.to_dict() for t in tokens])
    table = pt.Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()
    canvas1.update_idletasks()
    canvas1.config(scrollregion=canvas1.bbox('all'))

    # Perform parsing
    node, errors = parse(tokens)
    
    # Create a DataFrame from parsing errors
    error_df = pd.DataFrame(errors)
    
    # Display error list as a table in a new window
    error_list_window = tk.Toplevel()
    error_list_window.title('Error List')
    error_list_table = pt.Table(error_list_window, dataframe=error_df, showtoolbar=True, showstatusbar=True)
    error_list_table.show()
    
    # Draw the parse tree
    node.draw()

canvas1.pack(side='left', fill='both', expand=True)
scrollbar = tk.Scrollbar(root, command=canvas1.yview)
scrollbar.pack(side='right', fill='y')
canvas1.config(yscrollcommand=scrollbar.set)


frame = tk.Frame(canvas1)
canvas1.create_window((0, 0), window=frame, anchor='nw')


label1 = tk.Label(frame, text='Ultimate Prolog Parser')
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
