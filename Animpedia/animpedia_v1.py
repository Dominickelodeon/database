"""
/****************************************************************
*                                                               *
* Author: Jahi Miller                                           *
*  Title: Animpedia v1                                          *
*                                                               *
*  Description: This application allows for the                 *
*  adding of Anime Character information to a database file.    *
*  The program then displays database records in the viewer on  *
*  the Right of the form input fields.                          *
*                                                               *
****************************************************************/
"""

from tkinter import *
from tkinter import ttk
import sqlite3

######################### Python METHODS SECTION ###################################

# Connect to Database
def create_connection(pathToDataBase):
    connection = None
    try:
        connection = sqlite3.connect(pathToDataBase)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        return false

def execute_read_query(connection, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_drop():
    print('dropping')
    if not execute_query(connection,'drop table CHARACTERS'):
        cursor.execute(characters_table)


######################### SQL CREATE TABLE SECTION ###################################

characters_table = """
CREATE table if not exists CHARACTERS (
    id integer primary key,
    character text,
    title text,
    ability text,
    birthday text,
    sex text,
    fan text
);
"""

######################### SQL + PYTHON SECTION ###################################

def load_viewer(): #updates the viewer widget
    try:
        cursor.execute('Select character,title,ability,birthday,sex,fan from CHARACTERS')

        update_viewer(cursor)
        
        connection.commit()
        cursor.close
    except ValueError:
        pass

        
def post(*args):
    try:
        cursor.execute(characters_table)
        
        profile = (character.get(),title.get(),ability.get(),birthday.get(), sex.get(),fan.get())
        cursor.execute("INSERT into CHARACTERS(character,title,ability,birthday,sex,fan) values (?,?,?,?,?,?)", profile)
        
        connection.commit()
        cursor.close

        load_viewer()
    except ValueError:
        pass

def drop(*args):
    execute_drop()
    update_viewer('')
    

###########################################################
################ TKINTER WINDOW SECTION ###################
###########################################################
    
#ROOT Setup
root = Tk()
root.title("ANIMPEDIA")
root.resizable(False, False)
root.after_idle(load_viewer)

#MainFrame Window 
window = ttk.Frame(root, padding="3 3 12 12", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#Inconveniencing piece of code
connection = create_connection('animpedia_db.sqlite3')
cursor = connection.cursor() #represents the db connection
cursor.execute(characters_table) #creates the db table []


#Input Variables
character_var = StringVar()
title_var = StringVar()
ability_var = StringVar()
birthday_var = StringVar()
sex_var = StringVar()
fan_var=StringVar()

#Input Fields[Left Side]
character_lbl = ttk.Label(window, text="Character name: ")
character_lbl.grid(column=1, row=0, sticky=W)
character = ttk.Entry(window, textvariable=character_var)
character.grid(column=1, row=1, sticky='we',columnspan=3)

title_lbl = ttk.Label(window, text="Anime/Manga title: ")
title_lbl.grid(column=1, row=2, sticky=W)
title = ttk.Entry(window, textvariable=title_var)
title.grid(column=1, row=3, sticky='we', columnspan=3)


ability_lbl = ttk.Label(window, text="Ability(ies): ")
ability_lbl.grid(column=1, row=4, sticky=W)
ability = ttk.Entry(window, textvariable=ability_var)
ability.grid(column=1, row=5, sticky='we', columnspan=3)

birthday_lbl = ttk.Label(window, text="birthday: ")
birthday_lbl.grid(column=1, row=6, sticky=W)
birthday = ttk.Entry(window, textvariable=birthday_var, width=15)
birthday.grid(column=1, row=7, sticky='we', columnspan=2)

sex_lbl = ttk.Label(window, text="sex: ")
sex_lbl.grid(column=3, row=6, sticky=W)
sex = ttk.Entry(window, textvariable=sex_var, width=3)
sex.grid(column=3, row=7, sticky='we')

fan_lbl = ttk.Label(window, text="Fan name: ")
fan_lbl.grid(column=1, row=8, sticky=W)
fan = ttk.Entry(window, textvariable=fan_var, width=3)
fan.grid(column=1, row=9, sticky='we',columnspan=3)

#Buttons [Left Side]
drop_btn = ttk.Button(window, text="DROP", command=drop)
drop_btn.grid(column=3, row=10, sticky=W)

#rand_btn = ttk.Button(window, text="UPDATE")
#rand_btn.grid(column=2, row=8, sticky=W)
#rand_btn.configure(state='disabled')

post_btn = ttk.Button(window, text="POST", command=post, width=12)
post_btn.grid(column=1, row=10, sticky='we')

######################### CENTER SECTION ###################################

#Vertical Divider [Center]
divider = ttk.Separator(window, orient=VERTICAL)
divider.grid(column=4, row=0, rowspan=9, sticky='ns')

def empty_fields():
    character.delete(0, END)
    title.delete(0, END)
    ability.delete(0, END)
    birthday.delete(0, END)
    sex.delete(0, END)

######################### RIGHT SECTION ###################################

#Record Container [Right]
#view of the records as they are added
"""
viewer = Listbox(window, width=40, height=10)
viewer.grid(column=5, row=0, rowspan=9, sticky='ns')
"""

viewer = Text(window, width=50, height=10)
viewer.grid(column=5, row=0, rowspan=9, sticky='ns')#expands it from top to bottom
viewer.configure(state="disabled") #disables the textbox so users cannot make changes

def update_viewer(characters): #called by load_viewer()
    
    viewer.configure(state="normal") #enables the textbox so that the program make changes
    viewer.delete("0.0","end") #deletes everything in the textbox

    if characters:
        for row in characters:
            message = str(row) + "\n" 
            viewer.insert('end', message)
            print(message)        
    
    empty_fields()
    viewer.configure(state="disabled")
        
root.mainloop()
