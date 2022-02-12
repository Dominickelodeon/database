
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

import os
from pathlib import Path

#from PIL import ImageTk, Image

characters_table = """
CREATE table if not exists CHARACTERS (
    id integer primary key,
    name text,
    last_name text,
    cohort text,
    pod text,
    comment text
);
"""

#ROOT Setup
root = Tk()
root.title("Stipend_data")
root.resizable(False, False)
#root.after_idle(load_viewer)

#MainFrame Window 
window = ttk.Frame(root, padding="5", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#Input Variables
name_var = StringVar()
date_var = StringVar()
assingnment_var = StringVar()
credit_var = StringVar()
debit_var = StringVar()
comment_var=StringVar()

#Input Fields[Left Side]
name_lbl = ttk.Label(window, text="Name: ")
name = ttk.Entry(window, textvariable=name_var)
name_lbl.grid(column=1, row=0, sticky=W)
name.grid(column=1, row=1, sticky='we',columnspan=3)

date_lbl = ttk.Label(window, text="date: ")
date = ttk.Entry(window, textvariable=date_var)
date_lbl.grid(column=1, row=2, sticky=W)
date.grid(column=1, row=3, sticky='we',columnspan=3)

assingnment_lbl = ttk.Label(window, text="assingment: ")
assingnment = ttk.Entry(window, textvariable=assingnment_var)
assingnment_lbl.grid(column=1, row=4, sticky=W)
assingnment.grid(column=1, row=5, sticky='we',columnspan=3)

credit_lbl = ttk.Label(window, text="credit: ")
credit = ttk.Entry(window, textvariable=credit_var)
credit_lbl.grid(column=1, row=6, sticky=W)
credit.grid(column=1, row=7, sticky='we',columnspan=3)

debit_lbl = ttk.Label(window, text="debit: ")
debit = ttk.Entry(window, textvariable=debit_var)
debit_lbl.grid(column=1, row=8, sticky=W)
debit.grid(column=1, row=9, sticky='we',columnspan=3)

comment_lbl = ttk.Label(window, text="comment: ")
comment = ttk.Entry(window, textvariable=comment_var)
comment_lbl.grid(column=1, row=10, sticky=W)
comment.grid(column=1, row=11, sticky='we',columnspan=3)
