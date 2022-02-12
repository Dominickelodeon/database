################################################################
# Author;       Eugene Lemon                                   #
# Date;         11/21/2021                                     #
# Description;  This Python Source file will be used           #
#               with The Hidden Geniuse Project's OAK9         #
#               Database Rotation Fall 2021. It demonstrates   #
#               how to Connect to an SQLite Database, Create   #
#               a Table, Add rows to the table, Return rows to #
#               be displayed and Delete a table                #
#                                                              #
# Examine the attached code below to get an understanding on   #
# how to connect to and send queries to a SQL Database.  You   #
# will use this file to help you complete assignment #07.      #
################################################################

# Import necessary Libraries and Objects
import sqlite3
from sqlite3 import Error



#******** Function Definitions *****************#

# Connect to Database
def create_connection(pathToDataBase):
    connection = None
    try:
        connection = sqlite3.connect(pathToDataBase)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        
    return connection

# Execute Queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Query executed successfully")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        
#************ End Function Definition *******************

        
#************ Program Starting Point ********************

#************ Create Query Strings  *************#

# Create Staff Table Query String
create_staff_member_table_query = """
CREATE TABLE IF NOT EXISTS staff (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  cell TEXT NOT NULL,
  position TEXT NOT NULL
);
"""

# Insert Staff Members Into Staff Table Query String
add_staff_members_query = """
INSERT INTO
  staff (name,cell,position)
VALUES
  ('Baba','510.205.0980','Senior Innovation Educator'),
  ('Brandon','111.111.1111', 'Executive Director'),
  ('Hodari','(510) 435-2594','Curriculum Lead'),
  ('Akeeem','(415) 684-0505','Programs Director');
"""

# Display All Records In Staff Table Query String
display_staff_query = "SELECT * from staff"
        
# Connect to Existing or Create the Sqlite3 Database File
connection = create_connection("toDataBase")

# Execute query to create table
execute_query(connection, create_staff_member_table_query) 

# Execute Query to Insert Data
execute_query(connection, add_staff_members_query)

# Return results from select query
staff_members = execute_read_query(connection, display_staff_query)

# Print each employee's info
for employee in staff_members:
  print(employee)

# Delete the Staff Table
execute_query(connection,'drop table staff')
