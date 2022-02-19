## importing lib modules
from datetime import date
from selectors import EpollSelector
import sqlite3 as sql   # db to store and retrieve notes
from tkinter import *   # to create UI - contains widgets and input text fields
from tkinter import messagebox  # to display prompts eg popups to user

## creating db connection
try:
    con = sql.connect('post_it_notes.db')   # creates db to contain tables, connects to db
    cur = con.cursor()  # cursor object allows to execute query etc
    cur.execute('''CREATE TABLE notesTable 
        (date text, notesTitle text, notes text)''')    # execute executes given SQL statement, text accepts num, sym, lett
except:
    print("Connected to table of database") # db connection and table creation executes if not exists, else, just goes on

## defining functions

#insert row of data
def addNotes(): 
    # get input values
    today = dateEntry.get()
    notesTitle = notesTitleEntry.get()
    notes = notesEntry.get("1.0", "end-1c") # need to specify index for a text widget

    # raise prompt for missing inputs
    if len(today) <= 0 and len(notesTitle) <= 0 and len(notes) <= 0:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    else:
        # insert into table
        cur.execute("IMSERT INTO notesTable VALUES ('%s', '%s', '%s')" %(today, notesTitle, notes))
        messagebox.showinfo(message="Note added")
        con.commit()

# display all the notes in db
def view_notes():
    # read all the user input from entry widgets
    date = dateEntry.get()
    notesTitle = notesTitleEntry.get()

    # if no input is given, retrieve all notes
    if len(date) <= 0 and len(notesTitle) <= 0:
        sqlStatement = "SELECT * FROM notesTable"
    # if given title, retrieve notes matching title
    elif len(date) <= 0 and len(notesTitle) > 0:
        sqlStatement = "SELECT * FROM notesTable WHERE notesTitle = '%s'" %notesTitle
    # if given date, retrieve notes matching a date
    elif len(date) > 0 and len(notesTitle) <= 0:
        sqlStatement = "SELECT * FROM notesTable WHERE date = '%s'" %date
    # if given both, retrieve notes matching date and title
    else:
        sqlStatement = "SELECT * FROM notesTable WHERE date = '%s' AND notesTitle = '%s'" %(date, notesTitle)

    # execute the sql query
    cur.execute(sqlStatement)
    # obtain all query results, returns list in tuples
    row = cur.fetchall()
    # check if no query results retrieved
    if len(row) <0:
        messagebox.showerror(message="No note found")
    else:
        # print notes
        for i in row:
            messagebox.showinfo(message="Date:" + i[0] + "\nTitle:" + i[1] + "\nNotes:" + i[2])
        
# delete notes in post it note app
def deleteNotes():
    # obtain input values
    date = dateEntry.get()
    notesTitle = notesTitleEntry.get()
    # ask if user wants to delete all notes
    choice = messagebox.askquestion(message="Do you want to delete all notes?")
    # if select yes, delete all
    if choice == 'yes':
        sqlStatement = "DELETE FROM notesTable"
    else:
        # delete notes matching certain date and title
            if len(date) <= 0 and len(notesTitle) <0:
                # raise error for no inputs
                messagebox.showerror(message="ENTER REQUIRED DETAILS")
                return
            else:
                sqlStatement = "DELETE FROM notesTable WHERE date = '%s' AND notesTitle = '%s'" %(date, notesTitle)
    # execute sql query
    cur.execute(sqlStatement)
    messagebox.showinfo(message="Notes(s) deleted") #improvement - say number of rows deleted 
    con.commit()

# update existing notes
def update_notes():
    # get user input
    today = dateEntry.get()
    notesTitle = notesTitleEntry.get()
    notes = notesEntry.get("1.0", "end-1c")

    # check user input all values
    if len(today) <= 0 and len(notesTitle) <= 0 and len(notes) <= 1:
        messagebox.showerror(message="ENTER REQUIRED DETAILS")
    # update the note
    else:
        sqlStatement = "UPDATE notesTable SET nptes = '%s' WHERE date = '%s' and notesTitle = '%s'" %(notes, today, notesTitle)

    cur.execute(sqlStatement)
    messagebox.showinfo(message="Note updated")
    con.commit()

## creating user interface

# invoke call to class to view a window
window = Tk()
# set window dimensions and title
window.geometry("500x300")
window.title("Post-it Notes -Nuria Varela")
