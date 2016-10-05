import shutil
import os
import time
import datetime
from Tkinter import *
import tkFileDialog
import tkMessageBox
import sqlite3

dirName = ()
dirName2 = ()

def askdirectory():
  global dirName
  dirName = tkFileDialog.askdirectory()
  e1.insert (0, dirName)

def askdirectory2():
  global dirName2
  dirName2 = tkFileDialog.askdirectory()
  e2.insert (0, dirName2)

def fileCheckMove():
  src = dirName
  dst = dirName2
  now = datetime.datetime.now()
  date_str = dtm3
  dt_obj = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
  old = dt_obj
  fcmdt = [1, now]
  c.execute("INSERT OR REPLACE INTO MOD_INFO (ID, LAST_CHECK) VALUES (?, ?)", fcmdt)
  conn.commit()
  def get_table_data():
    c.execute("SELECT * FROM MOD_INFO")
    #print(c.fetchall()) 
  get_table_data()
  for root, dirs, files in os.walk(src):  
    for modFile in files:
      path = os.path.join(root, modFile)
      st = os.stat(path)    
      modTime = datetime.datetime.fromtimestamp(st.st_mtime)
      if modTime > old:
        if modFile.endswith(".txt"):
          srcFile = os.path.join(src, modFile)
          shutil.move(srcFile, dst)

def closeWindow (): 
  win.destroy()

def popup():
  tkMessageBox.showinfo("Completed","Files Check and Move Completed")
  closeWindow()

def completeMove():
  fileCheckMove()
  popup()

conn = sqlite3.connect('pyt60')
c = conn.cursor()
#conn.execute("DROP TABLE IF EXISTS MOD_INFO;") "Used for testing"
c.execute("CREATE TABLE IF NOT EXISTS MOD_INFO (ID INT PRIMARY KEY, LAST_CHECK DATETIME);")
c.execute("INSERT OR IGNORE INTO MOD_INFO(ID, LAST_CHECK) VALUES (1, '0001-01-01 00:00:00.000000');")
conn.commit()

win = Tk()
b1 = Button(win,text="Choose Source Folder:", command = askdirectory)
b2 = Button(win,text="Choose Desination Folder:",command = askdirectory2)
b1.grid(row = 0, column = 1, columnspan = 2, sticky = W, padx = 5, pady = 5)
b2.grid(row = 1, column = 1, columnspan = 2, sticky = W, padx = 5, pady = 5)

e1 = Entry(win, width = 50)
e2 = Entry(win, width = 50)
e1.grid(row = 0, column = 3, columnspan = 2, padx = 5, pady = 5)
e2.grid(row = 1, column = 3, columnspan = 2, padx = 5, pady = 5)

b3 = Button(win,text="File Check and Move", command = completeMove)
b3.grid(row = 2, column = 4, padx = 5, pady = 5, sticky = E)

c.execute("SELECT LAST_CHECK FROM MOD_INFO WHERE ID = 1")
dtm = c.fetchone()
dtm2 = str(dtm)
dtm3 = dtm2[3:][:-10]
lastCheck = "Last File Check: " + dtm3
l1 = Label(win, text = lastCheck)
l1.grid(row = 2, column = 1, padx = 5, pady = 5)
#print dtm3 "Used for testing"
win.mainloop()


            
''' Below prints to Shell to check if src & dst variables are correct and which files moved.

print src
print dst
moved = os.listdir(dst)
for file in moved:
   if file.endswith(".txt"):
       print dst + "\\" + os.path.normpath(file)
'''
