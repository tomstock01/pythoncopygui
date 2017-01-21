# Python Version 3.5.2
# Author: Tom Stock
# Purpose: Create a GUI that allows users to browse for a folder with files
#          and copy files that were modified in the last 24 hours to another folder.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import time
import datetime
import shutil
import sqlite3

class CopyFileGUI:
    def __init__(self, master):
       

        
### Frame        
        master.geometry('500x350') #(WidthxHeight)
        master.title("File Copy")
        
        master.resizable(False,False)
        self.now = time.time()

        
### Widgets
        instructions = Message(master, text = '''Welcome to the File Copy Application! \n\nTo use this form correctly follow these instructions:\n\n1) Select a Source Folder using the "Browse Source Folder..." button.\n\n2) Select a Destination Folder using the "Browse Destination Folder..." button.\n\n3) Click the "Copy Recent Files!" button to copy files that have been modified in the last 24 hours from the "From Folder:" to the "To Folder:"\n\nHappy copying!''',width = 450)
        instructions.grid(row = 0, column = 0, columnspan = 2, padx = 10)

        self.fromfolderLabel = ttk.Label(master, text = 'From Folder: ')
        self.fromfolderLabel.grid(row = 1, column = 0, padx = 5, sticky = 'sw')
        
        self.fromfolderButton = ttk.Button(master, text='Browse Source Folder ...', command = lambda : self.selectDir(self.fromfolderEntry))
        self.fromfolderButton.grid(row = 1, column = 1, sticky = 'e', padx = 5)
       
        self.fromfolderEntry = Entry(master, width = 80)
        self.fromfolderEntry.grid(row=2, column = 0, columnspan = 2, padx = 5)


        
        self.tofolderLabel = ttk.Label(master, text = 'To Folder: ')
        self.tofolderLabel.grid(row = 3, column = 0, padx = 5, sticky = 'sw')
        
        self.tofolderButton = ttk.Button(master, text='Browse Destination Folder...', command = lambda : self.selectDir(self.tofolderEntry))
        self.tofolderButton.grid(row = 3, column = 1, sticky = 'e', padx = 5)

        self.tofolderEntry = Entry(master, width = 80)
        self.tofolderEntry.grid(row = 4, column = 0, columnspan = 2, padx = 5)

        self.copyfilesButton = ttk.Button(master, text = 'Copy Recent Files!')
        self.copyfilesButton.grid(row = 5, column = 0, columnspan = 2, pady =10)
        self.copyfilesButton.bind('<ButtonPress>', self.copyclicked)

        self.v = StringVar()
        self.lastCopyLabel = ttk.Label(master, textvariable = self.v)
        self.v.set('Last copy performed on: ')# + self.display_latest()[0])       
        self.lastCopyLabel.grid(row = 6, column = 0, columnspan = 2)
                                            

### sqlite3
        self.conn = sqlite3.connect('timestamps.db')
        self.c = self.conn.cursor()
        self.create_table()
        

        
    def create_table(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS copyTimes (epochTime REAL, datestamp TEXT)')
        self.c.execute('SELECT * FROM copyTimes')
        if self.c.fetchall() == []:
            self.c.execute("INSERT INTO copyTimes (epochTime, datestamp) VALUES(0.0, '2017-01-18')")
            self.v.set("Database has not yet been populated")
            self.conn.commit()
        else:
            self.v.set("Last copy performed on: " + self.display_latest()[0])
            self.conn.commit()
        self.c.close()
        self.conn.close() 

    def copyTime_entry(self):
        self.conn = sqlite3.connect('timestamps.db')
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO copyTimes (epochTime, datestamp) VALUES (?, ?)", (self.now, str(time.strftime('%Y-%m-%d %H:%M:%S'))))
        self.conn.commit()
        self.c.close()
        self.conn.close()

    def display_latest(self):
        self.conn = sqlite3.connect('timestamps.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT datestamp FROM copyTimes ORDER BY datestamp DESC')
        mostRecent = self.c.fetchone()
        #self.c.close()
        #self.conn.close()
        return (mostRecent)

                    
        
### Functions
    def selectDir(self, dirName):
        folder = filedialog.askdirectory()
        dirName.config(state = NORMAL)
        dirName.delete(0,END)
        dirName.insert(0,folder + '/')
        dirName.config(state = 'readonly')
            
    def filecopy(self, src, dst):
        now = time.time()  # gets current time
        docs = os.listdir(src) # searches source folder for documents in it
        for i in docs:
            y = src + i # gets complete file path from the folder with the documents
            modtime = os.stat(y).st_mtime # reads the last modified date of each file
            past24 = (now - 86400)  # gets the time of 24 hours ago
            if modtime > past24:  # compares the last modified time vs 24 hours ago
                shutil.copy(y, dst) # copies file that were modified within last 24 hours
                print (y)
               
    def doit(self):
        fromFolder = self.fromfolderEntry.get()
        toFolder = self.tofolderEntry.get()
        self.filecopy(fromFolder, toFolder)
        self.copyTime_entry()
        self.v.set('Last copy performed on: ' + self.display_latest()[0])        

    def copyclicked(self, event): # Performs copying function and produces a confirmation messagebox
        self.doit()
        messagebox.showinfo(title = "You did it!", message = "Files successfully copied!")
        self.display_latest()
                

def main():
    root = Tk()
    copyfileGUI = CopyFileGUI(root)
    root.mainloop()

if __name__ == "__main__":main()
    
    
