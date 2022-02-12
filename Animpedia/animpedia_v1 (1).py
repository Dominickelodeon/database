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

import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

import os
from pathlib import Path

from PIL import ImageTk, Image

######################### SQL METHODS SECTION ###################################

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

def execute_drop():
    print('dropping')
    if not execute_query(connection,'drop table CHARACTERS'):
        cursor.execute(characters_table)
        

def execute_read_query(connection, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


######################### SQL TABLE SECTION ###################################

#DB Query that creates the database and defines the Table Columns and Data Types
characters_table = """
CREATE table if not exists CHARACTERS (
    id integer primary key,
    character text,
    title text,
    ability text,
    birthday text,
    sex text,
    icon_image blob
);
"""

######################### SQL + PYTHON SECTION ###################################

#Record Dictionary that holds the Image objects, and row info
record = {} #defines the global var datatype as dictionary

#loads the viewer widget
def load_viewer():
    try:
        cursor.execute('Select * from CHARACTERS')

        update_viewer(cursor)
        
        connection.commit()
        cursor.close
    except ValueError:
        pass

#Retrieves the data from the form inputs;
#Sends the data to the Database
def post(*args):
    try:
        cursor.execute(characters_table)
        
        profile = (character.get(),title.get(),ability.get(),birthday.get(), sex.get(), icon_fileb)
        print(len(profile))
        cursor.execute("INSERT into CHARACTERS(character,title,ability,birthday,sex,icon_image) values (?,?,?,?,?,?)", profile)
        
        connection.commit()
        cursor.close

        load_viewer()
    except ValueError:
        pass

#Drops/Deletes the Table from the database
#Updates the Viewer Widget by removing all sub-elements from the viewer
def drop(*args):
    execute_drop()
    update_viewer()

    
### Image Handling Blob ###
    
#converts file to BLOB (Binary Large Object)
def convert_binary(file_name):
    binary_data = None
    #Opens file and Reads its data as binary
    with open(file_name, 'rb') as b_file: #creates an instance of the file
        binary_data = b_file.read()
    return binary_data #returns file contents as binary data
 
#Injects BLOB (Binary Large Object) into Image file
def convert_file(file_name, data):
   with open(file_name, 'wb') as b_file:
       b_file.write(data)

#Retrieves/Creates path to parent folder
def folder_path():
    #Retrieves current path to parent folder
    parent_folder = Path(__file__).parent
    directory = "icon_images"
    path = os.path.join(parent_folder, directory) #adds new folder to string path.

    #Creates the icon_images folder if it does not already exist
    if not os.path.isdir(path):
        os.mkdir(path)
    return path

#removes all files from the icon_images folder
def remove_file():
    #Retrieves and Loops through all files with certain characteristics
    for f in Path(folder_path()).glob("*"):
        if f.is_file(): #checks if item is file
            f.unlink() #removes item from folder

#Handle image data retrieved from db
#downloads the files to the icon_images folder if not already present
#Stores an instance of the image object in the 'record' dictionary so that it does not get garbage collected
def format_image_file(row, w=34, h=26):
    if row[-1]:
        img_addrs = "{0}//icon_image_{1}_{2}.jpg".format(folder_path(),row[1], row[0])
        if not os.path.isfile(img_addrs):
            convert_file(img_addrs,row[-1]) #converts byte data into image file

        record[str(row[0])] = Image.open(img_addrs).resize((w, h), Image.ANTIALIAS)#.resize(w, h) sets the size of the image
        record[str(row[0])] = (ImageTk.PhotoImage(record[str(row[0])]), row[:-1])

#Creates global variable [icon_fileb] which is used in (post function)
def upload_image():
    global icon_fileb
    #opens finder and only allows the selection of files with specific file types 
    filename = fd.askopenfilename(filetypes = [("Image Files","*.png"),("Image Files","*.jpg"), ("Image Files","*.jpeg")])
    icon_fileb = convert_binary(filename) #converts file to binary data and assigns data to global

    if icon_fileb: #checks if file is uploaded;
        #disables upload btn and changes text 
        upload_btn.configure(state='disabled', text="image uploaded")        
    
    
### Variable Declaration ####

#Inconveniencing piece of code
connection = create_connection('animpedia_dbV1.sqlite3')
cursor = connection.cursor() #represents the db connection
cursor.execute(characters_table) #creates the db table []

###########################################################
################ TKINTER WINDOW SECTION ###################
###########################################################
    
#ROOT Setup
root = Tk()
root.title("ANIMPEDIA")
root.resizable(False, False)
root.after_idle(load_viewer)

#MainFrame Window 
window = ttk.Frame(root, padding="5", width=400, height=250)
window.grid(column=0, row=0, sticky=(N, W, E, S))

#Input Variables
character_var = StringVar()
title_var = StringVar()
ability_var = StringVar()
birthday_var = StringVar()
sex_var = StringVar()

#Input Fields[Left Side]
character_lbl = ttk.Label(window, text="Character name: ")
character = ttk.Entry(window, textvariable=character_var)
character_lbl.grid(column=1, row=0, sticky=W)
character.grid(column=1, row=1, sticky='we',columnspan=3)

title_lbl = ttk.Label(window, text="Anime/Manga title: ")
title = ttk.Entry(window, textvariable=title_var)
title_lbl.grid(column=1, row=2, sticky=W)
title.grid(column=1, row=3, sticky='we', columnspan=3)

ability_lbl = ttk.Label(window, text="Ability(ies): ")
ability = ttk.Entry(window, textvariable=ability_var)
ability_lbl.grid(column=1, row=4, sticky=W)
ability.grid(column=1, row=5, sticky='we', columnspan=3)

birthday_lbl = ttk.Label(window, text="birthday: ")
birthday = ttk.Entry(window, textvariable=birthday_var, width=15)
birthday_lbl.grid(column=1, row=6, sticky=W)
birthday.grid(column=1, row=7, sticky='we', columnspan=2)

sex_lbl = ttk.Label(window, text="sex: ")
sex = ttk.Entry(window, textvariable=sex_var, width=3)
sex_lbl.grid(column=3, row=6, sticky=W)
sex.grid(column=3, row=7, sticky='we')

#Buttons [Left Side]

upload_btn = ttk.Button(window, text="upload image", command=upload_image)
upload_btn.grid(column=1, row=8, sticky='we', columnspan=3)

post_btn = ttk.Button(window, text="POST", command=post, width=12)
post_btn.grid(column=1, row=9, sticky='we')

drop_btn = ttk.Button(window, text="DROP", command=drop)
drop_btn.grid(column=3, row=9, sticky=W)

def empty_fields():
    character.delete(0, END)
    title.delete(0, END)
    ability.delete(0, END)
    birthday.delete(0, END)
    sex.delete(0, END)
    upload_btn.configure(state='normal', text="upload image")

######################### CENTER SECTION ###################################

#Vertical Divider [Center]
divider = ttk.Separator(window, orient=VERTICAL)
divider.grid(column=4, row=0, rowspan=10, padx=(5, 5), sticky='ns')

######################### RIGHT SECTION ###################################

#Record Container [Right]
#view of the records as they are added

viewer = Text(window, width=50, height=10, exportselection=0)
viewer.grid(column=5, row=0, rowspan=9, columnspan=2, sticky='ns')#expands it from top to bottom
viewer.configure(state="disabled") #disables the textbox so users cannot make changes

def update_viewer(characters=None, item=None): #called by load_viewer()
    viewer.configure(state="normal") #enables the textbox so that the program make changes
    viewer.delete("0.0","end") #deletes everything in the textbox
    
    if characters and not item:
        for row in characters:
            #adds the image to records list so that it does not get garbage collected
            format_image_file(row) 

        for index, items in record.items():
            #creates the displayed image in the Text Widget
            viewer.image_create(END, image=items[0])
            #Inserts the text elements into the Text widget and creates a new line
            viewer.insert('end', ": "+str(items[1])+"\n")

    if not characters and not item: #clears the record dict if None is passed
        record.clear() #this means if the table is the object will clear
        active = 0

    if item:
        viewer.image_create(END, image=item[0])
        viewer.insert('end', ": "+str(item[1])+"\n") 

    empty_fields()
    remove_file()
    viewer.configure(state="disabled")

#Buttons [Right Side]


back_btn = ttk.Button(window, text="BACK", command=lambda: toggle(False))
back_btn.grid(column=5, row=9, sticky='we')
#back_btn.configure(state='disabled')

next_btn = ttk.Button(window, text="NEXT", command=lambda: toggle(True))
next_btn.grid(column=6, row=9, sticky='we')

active = 0
def toggle(direction):
    global active

    if record:
        if direction and active < len(record):
            active+=1
        elif not direction and active > 1:
            active-=1

        update_viewer(None, record[str(active)])
        
root.mainloop()
