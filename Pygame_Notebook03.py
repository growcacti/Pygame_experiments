import tkinter as tk
#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import filedialog
from tkinter import Tk, Frame, Button, BOTH, SUNKEN
from tkinter.colorchooser import askcolor

# from tkinter import font
import tkinter.font as tkFont

# from tkinter.scrolledtext import *
import pyautogui as pg
import pyperclip
import os
import sys

# import subprocess
# import shutil
import pathlib
from PIL import Image, ImageTk
import runpy
import glob
import time


from tkinter.scrolledtext import ScrolledText 
import os, sys, subprocess

root = Tk()
root.geometry('1500x800')
notebook = ttk.Notebook(root)

notebook.grid(row=0, column=0)

frame1 = ttk.Frame(notebook)

def opensystem(event):

    x = lb.curselection()[0]

    file = lb.get(x)
    with open(file, "r") as file:
        file = file.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, file)

        return


def showcontent(x):

    lb.focus()
    x = lb.curselection()[0]
    file = lb.get(x)
    with open(file, "r") as file:
        file = file.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, file)

        return

def run(event):

    file = lb.get(ANCHOR)
    runpy.run_module(file)

    return


def open_file(textwidget, frame):
    '''Open a file for editing.'''
    filepath = askopenfilename(
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
    )
    if not filepath:
        return
    textwidget.delete(1.0, tk.END)
    with open(filepath, 'r') as input_file:
        text = input_file.read()
        textwidget.insert(tk.END, text)
    root.title(f'Simple Text Editor - {filepath}')

def save_file():
    '''Save the current file as a new file.'''
    filepath = asksaveasfilename(
        defaultextension='txt',
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
    )
    if not filepath:
        return
    with open(filepath, 'w') as output_file:
        text = textwidget.get(1.0, tk.END)
        output_file.write(text)
    root.title(f'Simple Text Editor - {filepath}')

def newdirlist():
    a = "/home/jh/Desktop/Codeview_Project/"

    path = filedialog.askdirectory(initialdir=a)
    os.chdir(path)
    flist = os.listdir(path)
    lb.delete(0, tk.END)

    for item in flist:

        lb.insert(tk.END, item)
    return flist

def clear(textwidget, frame):
    textwidget_edit.delete("1.0", tk.END)


def ggtxt(textwidget, frame):
    a = text.get("1.0", tk.END)
    textwidget.insert(tk.END, a)


def ggtxt2():
    a = text2.get("1.0", tk.END)
    txt_edit.insert(tk.END, a)

##frame1.rowconfigure(0, minsize=800, weight=5)
##frame1.columnconfigure(1, minsize=800, weight=5)
frlist = tk.Frame(frame1)
frlist.grid(row=1, column=1)
##frlist.rowconfigure(0, minsize=800, weight=1)
##frlist.columnconfigure(1, minsize=800, weight=1)
lb = tk.Listbox(frlist, bg="cornsilk",bd=12,width=35, height=40, exportselection=False, selectmode=tk.MULTIPLE)
lb.grid(row=1, column=2, rowspan=3, sticky="nswe")
lb.focus()
lb.configure(selectmode="")
flist = os.listdir()

for item in flist:
##    item.split(name, ext)
##    ext = ".py", ".txt"
    lb.insert(tk.END, item)
lb.bind("<Double-Button-1>", opensystem)
lb.bind("<<ListboxSelect>>", showcontent)
lb.bind("<Double-Button-2>", run)


text = ScrolledText(frame1,
                      bg='white',
                      bd=12,
                      relief=GROOVE,
                      height=50,
                      width=180,
                      font='TkFixedFont',)
text.grid(row = 1, column=5)
  
fr_buttons = tk.Frame(frame1, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open', bd=8, command= lambda:open_file(txt, frame1))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=8,   command= lambda:save_file(txt, frame1))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)
btn14 = tk.Button(fr_buttons, text="get dir", bd=8, command=newdirlist)
btn14.grid(row=3, column=0)
btn11 = tk.Button(fr_buttons, text="RUN", bd=8,command=run)
btn11.grid(row=4, column=0)

fr_buttons.grid(row=1, column=0, sticky='ns')


def ggtxtany(textwidget):
    a = text2.get("1.0", tk.END)
    textwidget.insert(tk.END, a)


def open3():

    top = tk.Toplevel(root)
    '''Open a file for editing.'''
    tk.Label(top, text='Select number of textbox for operation').grid(row=0, column=0)
    
    cb = ttk.Combobox(top, values=['2', '3', '4','5','6','7','8','9'])
    cb.grid(row=1, column=0)
   

    w = cb.get()
    if w == 2:
        txtbox = text2
    elif w == 3:
        txtbox = text3
    elif w == 4:
        txtbox = text4
    elif w == 5:
        txtbox = text5
    elif w == 6:
        txtbox = text6
    elif w == 7:
        txtbox = text7
    elif w == 8:
        txtbox = text8
    elif w == 9:
        txtbox = text9
    else:
        pass
    cb.bind('<<ComboboxSelected>>', lambda x: open(cb.get()))
    def open(txtbox):
            
        filepath = filedialog.askopenfilename(
        filetypes=[('Python Files'), ('*.py'), ('Text Files', '*.txt'), ('All Files', '*.*')])
        if not filepath:
            return
        txtbox.delete(1.0, tk.END)
        with open(filepath, 'r') as input_file:
            text = input_file.read()
            txtbox.insert(tk.END, text)
            
    btntop = tk.Button(top, text='text widget Selection',  command= lambda:lambda: open3())
    btntop.grid(row=2, column=0)

















frame2 = ttk.Frame(notebook)



frame2.rowconfigure(0, minsize=800, weight=1)
frame2.columnconfigure(1, minsize=800, weight=1)

txt2_edit = ScrolledText(frame2)
fr_buttons = tk.Frame(frame2, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open', bd=6, command= lambda:open_file(txt2_edit, frame2))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=6, command= lambda:save_file(txt2_edit, frame2))
btn_grab =tk.Button(fr_buttons, text='Grab from F1...', bd=6, command= lambda: ggtxt(txt2_edit, frame2))
btn_grab.grid(row=2, column=0)
btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')
txt2_edit.grid(row=0, column=1, sticky='nsew')
notebook.add(frame1, text='1')
notebook.add(frame2, text='2')
f3 = ttk.Frame(notebook)
notebook.add(f3, text='3')
text3 = ScrolledText(f3, height=54, width=160, bd=10, bg='wheat')
text3.insert('1.0', tk.END)
text3.grid(row=0, column=4, rowspan=25, columnspan=10)
fr_btn = tk.Frame(f3, relief=tk.RAISED, bd=10)
btn_open = tk.Button(fr_btn, text='Open', bd=6, command= lambda:open_file(text3, f3))
btn_save = tk.Button(fr_btn, text='Save As...', bd=6, command= lambda:save_file(text3, f3))
btn_grab =tk.Button(fr_btn, text='Grab from F1...', bd=6, command= lambda: ggtxt(text3, f3))
btn_grab.grid(row=2, column=0)
btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)
fr_btn.grid(row=0, column=0, sticky='ns')

f4 = ttk.Frame(notebook)
notebook.add(f4, text='4')
f5 = ttk.Frame(notebook)
        
# Combobox creation


notebook.add(f5, text='5')
f6 = ttk.Frame(notebook)
notebook.add(f6, text='6')
f7 = ttk.Frame(notebook)
notebook.add(f7, text='7')
f8 = ttk.Frame(notebook)
notebook.add(f8, text='8')
f9 = ttk.Frame(notebook)
notebook.add(f9, text='9')
f10 = ttk.Frame(notebook)
notebook.add(f10, text='10')
f11 = ttk.Frame(notebook)
notebook.add(f11, text='11')
f12 = ttk.Frame(notebook)
notebook.add(f12, text='12')
f13 = ttk.Frame(notebook)
notebook.add(f13, text='13')
f14 = ttk.Frame(notebook)
notebook.add(f14, text='14')
f15 = ttk.Frame(notebook)
notebook.add(f15, text='15')
f16 = ttk.Frame(notebook)
notebook.add(f16, text='16')
notebook2 = ttk.Notebook(f16)

notebook2.grid(row=2, column=2)
ff1 = ttk.Frame(notebook2)
ff2 = ttk.Frame(notebook2)

notebook2.add(ff1, text='1')
notebook2.add(ff2, text='2')

ff3 = ttk.Frame(notebook2)
notebook2.add(ff3, text='3')
text33 = ScrolledText(ff3, height=50, width=100, bg='wheat' ,bd=10)
text3.insert('1.0', tk.END)
text33.grid(row=2, column=4, rowspan=25, columnspan=10)
ff4 = ttk.Frame(notebook2)
notebook2.add(ff4, text='4')
ff5 = ttk.Frame(notebook2)
        
# Combobox creation


notebook2.add(ff5, text='5')
ff6 = ttk.Frame(notebook2)
notebook2.add(ff6, text='6')
ff7 = ttk.Frame(notebook2)
notebook2.add(ff7, text='7')
ff8 = ttk.Frame(notebook2)
notebook2.add(ff8, text='8')
ff9 = ttk.Frame(notebook2)
notebook2.add(ff9, text='9')
ff10 = ttk.Frame(notebook2)
notebook2.add(ff10, text='10')
ff11 = ttk.Frame(notebook2)
notebook2.add(ff11, text='11')
ff12 = ttk.Frame(notebook2)
notebook2.add(ff12, text='12')
ff13 = ttk.Frame(notebook2)
notebook2.add(ff13, text='13')
ff14 = ttk.Frame(notebook2)
notebook2.add(ff14, text='14')
ff15 = ttk.Frame(notebook2)
notebook2.add(ff15, text='15')
f116 = ttk.Frame(notebook2)
notebook2.add(f116, text='116')

text10 = ScrolledText(f10, height=50, width=100, bg='wheat', bd=10)
text10.insert('1.0', tk.END)
text10.grid(row=0, column=4, rowspan=25, columnspan=10)

text4 = ScrolledText(f4, height=50, width=300, bg='wheat', bd=10)
text4.insert('1.0', tk.END)

text4.grid(row=0, column=4, rowspan=25, columnspan=10)
text5 = ScrolledText(f5, height=50, width=300, bg='white',bd=10)
text5.insert('1.0', tk.END)
text5.grid(row=0, column=4, rowspan=25, columnspan=10)
text6 = ScrolledText(f6, height=50, width=100, bg='white',bd=10)
text6.insert('1.0', tk.END)
text6.grid(row=0, column=4, rowspan=25, columnspan=10)
text7 = ScrolledText(f7, height=50, width=100, bg='light blue',bd=10)
text7.insert('1.0', tk.END)
text7.grid(row=0, column=4, rowspan=25, columnspan=10)
text8 = ScrolledText(f8, height=50, width=100, bg='pink',bd=10)
text8.insert('1.0', tk.END)
text8.grid(row=0, column=4, rowspan=25, columnspan=10)
text9 = ScrolledText(f9, height=50, width=100, bg='light green', bd=10)
text9.insert('1.0', tk.END)
text9.grid(row=0, column=4, rowspan=25, columnspan=10)


text11 = ScrolledText(f11, height=50, width=100, bg='wheat',bd=10)
text11.insert('1.0', tk.END)
text11.grid(row=0, column=4, rowspan=25, columnspan=10)

text12 = ScrolledText(f12, height=50, width=300, bg='wheat',bd=10)
text12.insert('1.0', tk.END)

text12.grid(row=0, column=4, rowspan=25, columnspan=10)
text13 = ScrolledText(f13, height=50, width=300, bg='white', bd=10)
text13.insert('1.0', tk.END)
text13.grid(row=0, column=4, rowspan=25, columnspan=10)
text14 = ScrolledText(f14, height=50, width=100, bg='white', bd=10)
text14.insert('1.0', tk.END)
text14.grid(row=0, column=4, rowspan=25, columnspan=10)
text15 = ScrolledText(f15, height=50, width=100, bg='light blue', bd=10)
text15.insert('1.0', tk.END)
text15.grid(row=0, column=4, rowspan=25, columnspan=10)



fr_buttons2 = tk.Frame(f10, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons2, text='Open',bd=6,  command= lambda:open_file(text10, f10))
btn_save = tk.Button(fr_buttons2, text='Save As...', bd=6, command= lambda:save_file(text10, f10))
def ggtxt2():
    a = text2.get("1.0", tk.END)
    txt_edit.insert(tk.END, a)

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)
btn_grab =tk.Button(fr_buttons2, text='Grab from F1...', bd=6,  command= lambda: ggtxt(text10, f10))
btn_grab.grid(row=2, column=0)
fr_buttons2.grid(row=0, column=0, sticky='ns')


fr_buttons3 = tk.Frame(f4, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons3, text='Open', bd=6, command= lambda:open_file(text4, f4))
btn_save = tk.Button(fr_buttons3, text='Save As...', bd=6, command= lambda:save_file(text4, f4))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons3.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(f5, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open', bd=6,  command= lambda:open_file(text5, f5))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=6,  command= lambda:save_file(text5, f5))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(f6, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open', bd=6,  command= lambda:open_file(text6, f6))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=6,  command= lambda:save_file(text6, f6))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(f7, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open', bd=6,  command= lambda:open_file(text7, f7))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(text7, f7))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(f8, relief=tk.RAISED, bd=6)
btn_open = tk.Button(fr_buttons, text='Open',bd=6,  command= lambda:open_file(text8, f8))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(text8, f8))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(f9, relief=tk.RAISED, bd=8)
btn_open = tk.Button(fr_buttons, text='Open', bd=8,  command= lambda:open_file(text9, f9))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=8,  command= lambda:save_file(text9, f9))



fr_buttons = tk.Frame(f11, relief=tk.RAISED, bd=8)
btn_open = tk.Button(fr_buttons, text='Open',bd=8,  command= lambda:open_file(text11, f11))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=8,  command= lambda:save_file(text11, f11))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(f12, relief=tk.RAISED, bd=8)
btn_open = tk.Button(fr_buttons, text='Open',bd=6,  command= lambda:open_file(text12, f12))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=6,  command= lambda:save_file(text12, f12))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(f13, relief=tk.RAISED, bd=8)
btn_open = tk.Button(fr_buttons, text='Open', bd=8,  command= lambda:open_file(text13, f13))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=8, command= lambda:save_file(text13, f13))
btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(f4, relief=tk.RAISED, bd=8)
btn_open = tk.Button(fr_buttons, text='Open', bd=8,  command= lambda:open_file(text15, f15))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=8,  command= lambda:save_file(text15, f15))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')


txt1 = ScrolledText(ff1, height=50, width=300, bg='wheat', bd=12)
txt1.insert('1.0', tk.END)
txt2= ScrolledText(ff2, height=50, width=300, bg='wheat', bd=12)
txt2.insert('1.0', tk.END)
txt3 = ScrolledText(ff4, height=50, width=300, bg='wheat', bd=12)
txt3.insert('1.0', tk.END)
txt4 = ScrolledText(ff4, height=50, width=300, bg='wheat', bd=12)
txt4.insert('1.0', tk.END)


txt4.grid(row=0, column=4, rowspan=25, columnspan=10)
txt5 = ScrolledText(ff5, height=50, width=300, bg='white', bd=12)
txt5.insert('1.0', tk.END)
txt5.grid(row=0, column=4, rowspan=25, columnspan=10)
txt6 = ScrolledText(ff6, height=50, width=100, bg='white', bd=12)
txt6.insert('1.0', tk.END)
txt6.grid(row=0, column=4, rowspan=25, columnspan=10)
txt7 = ScrolledText(ff7, height=50, width=100, bg='light blue', bd=12)
txt7.insert('1.0', tk.END)
txt7.grid(row=0, column=4, rowspan=25, columnspan=10)
txt8 = ScrolledText(ff8, height=50, width=100, bg='pink', bd=12)
txt8.insert('1.0', tk.END)
txt8.grid(row=0, column=4, rowspan=25, columnspan=10)
txt9 = ScrolledText(ff9, height=50, width=100, bg='light green',bd=12)
txt9.insert('1.0', tk.END)
txt9.grid(row=0, column=4, rowspan=25, columnspan=10)

txt10 = ScrolledText(ff10, height=50, width=300, bg='wheat', bd=12)
txt10.insert('1.0', tk.END)

txt10.grid(row=0, column=4, rowspan=25, columnspan=10)
txt11 = ScrolledText(ff11, height=50, width=300, bg='white', bd=12)
txt11.insert('1.0', tk.END)
txt11.grid(row=0, column=4, rowspan=25, columnspan=10)
txt12 = ScrolledText(ff12, height=50, width=100, bg='white', bd=12)
txt12.insert('1.0', tk.END)
txt12.grid(row=0, column=4, rowspan=25, columnspan=10)
txt13 = ScrolledText(ff13, height=50, width=100, bg='light blue', bd=12)
txt13.insert('1.0', tk.END)
txt13.grid(row=0, column=4, rowspan=25, columnspan=10)
txt14 = ScrolledText(ff14, height=50, width=100, bg='pink', bd=12)
txt14.insert('1.0', tk.END)
txt14.grid(row=0, column=4, rowspan=25, columnspan=10)
fr_buttons = tk.Frame(ff1, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open', bd=8,  command= lambda:open_file(txt1, ff1))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=8,  command= lambda:save_file(txt1, ff1))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')
txt1.grid(row=0, column=1, sticky='nsew')


fr_buttons = tk.Frame(ff2, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open',bd=9,  command= lambda:open_file(txt2, ff2))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=9,  command= lambda:save_file(txt2, ff2))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')
txt2.grid(row=0, column=1, sticky='nsew')



fr_buttons = tk.Frame(ff3, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open',bd=9, command= lambda:open_file(txt3, ff3))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=9,  command= lambda:save_file(txt3, ff3))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(ff4, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text='Open',  command= lambda:open_file(txt4, ff4))
btn_save = tk.Button(fr_buttons, text='Save As...',  command= lambda:save_file(txt4, ff4))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(ff5, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open', bd=8, command= lambda:open_file(txt5, ff5))
btn_save = tk.Button(fr_buttons, text='Save As...', bd=8,  command= lambda:save_file(txt5, ff5))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(ff6, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open', bd=6,  command= lambda:open_file(txt6, ff6))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(txt6, ff6))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(ff7, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open', bd=6, command= lambda:open_file(txt7, ff7))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(txt7, ff7))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')



fr_buttons = tk.Frame(ff8, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open',bd=6,  command= lambda:open_file(txt8, ff8))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(txt8, ff8))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(ff9, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text='Open',  command= lambda:open_file(txt9, ff9))
btn_save = tk.Button(fr_buttons, text='Save As...',  command= lambda:save_file(txt9, ff9))

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_buttons.grid(row=0, column=0, sticky='ns')




fr_buttons = tk.Frame(ff10, relief=tk.RAISED, bd=12)
btn_open = tk.Button(fr_buttons, text='Open', bd=6, command= lambda:open_file(txt10, ff10))
btn_save = tk.Button(fr_buttons, text='Save As...',bd=6,  command= lambda:save_file(txt10, ff10))
# disables the tab
# notebook.tab(0, state = 'disabled')
# entering and displaying multiple lines with the text widget

note_str = '''
import pygame as pg
import sys
import random
from pygame.locals import *
pg.init()
 
# Colours
WHITE = (255, 255, 255)
RED = (255,0,0)

# Game Setup
FPS = 60
clock = pge.time.Clock()
WIDTH = 1400
HEIGHT = 900
 
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('My Game!')
road = pg.Surface((1400, 400))
road.fill((30,30,30))
for i in range(1, 1400, 50):
  pg.draw.line(road,(255,2import pygame as pg



from pygame.locals import *      
import sys
 
# 1200 x 630

W = 300
H = 158
HW = W / 2
HH = H / 2


QW = HW / 4
QH = HH/  4

screen = pg.display.set_mode((1200, 800))
clock = pg.time.Clock()

bg_img = pg.image.load("gx/bg88.png") 




class Subsurf:

    def __init__(self, pos, size, image):
        self.image =image
        self.size = size
        self.pos = pos
        self.w, self.h = self.size
        self.x, self.y = self.pos
        self.make_subrect()

    def make_subrect(self):
        self.rect = pg.Rect(self.image.get_rect())
        self.sub_surf = self.image.subsurface(self.rect)
        self.surf= pg.Surface((2000, 2000))
        self.surf.blit(self.sub_surf, (HW,HH))
      
        return self.sub_surf, self.surf


##    def blit(self, sub_surf, x, y):
##        screen.blit(sub_surf, (self.x, self.y))    
##
i = 0
j = 0
 
pos = (400,800)
size = (HW, HH)

s = Subsurf(pos,size, bg_img)
ss = Subsurf(pos,size, bg_img)
ss2 = Subsurf(pos,size, bg_img)
ss3 = Subsurf(pos,size, bg_img)
#bg_img = pg.transform.scale(bg_img,(width,height))

 
loop = True
while loop:
    screen.fill((0,0,0))
##    screen.blit(bg_img,(i,j))
   
    screen.blit(bg_img,(QW, QH))
    screen.blit(s.sub_surf,(i, j))
    screen.blit(ss.sub_surf,((-i, -j)))
    screen.blit(ss2.sub_surf,(-i, j))
    screen.blit(ss2.sub_surf,(i, -j))
    for event in pg.event.get():
        if event.type == QUIT:
            loop = False
    i += 0.5
    j += 0.5
    pressed = pg.key.get_pressed()
     

    if pressed[pg.K_UP]:
        j-= 1
##        screen.blit(bg_img,(0, height+j))
      
    if pressed[pg.K_DOWN]:
        j += 1
##        screen.blit(bg_img,(0, height+j))
          
    if pressed[pg.K_LEFT]:
        i-= 5
##        screen.blit(bg_img,(width+i, 0))

    if pressed[pg.K_RIGHT]:
        i += 5
##        screen.blit(bg_img,(width + i, 0))     
    pg.display.update()
pg.quit()


55,255),(i,50), (i+20,50),4)
  pg.draw.line(road,(255,255,255),(i,150), (i+20,150),4)
  pg.draw.line(road,(255,255,255),(i,200), (i+200,200),10)
  pg.draw.line(road,(255,255,255),(i,250), (i+20,250),4)
  pg.draw.line(road,(255,255,255),(i,350), (i+20,350),4) 
  roadrect = pg.Rect(0,200,400,100)
# The main function that controls the game
def main():
  looping = True
  
  # The main game loop
  while looping :
    screen.fill((0,0,0,0))
  
    # Get inputs
    for event in pg.event.get() :
      if event.type == QUIT :
        pg.quit()
        sys.exit()
    
    # Processing
    # This section will be built out later
 
    # Render elements of the game
    screen.blit(road, roadrect)
    pg.display.update()
    clock.tick(FPS)
if  __name__ == '__main__':
    
    main()

'''
text4.insert(tk.END, note_str)

note_str33='''

button1 = pg.Rect(10, 10, 75, 25)
button2 = pg.Rect(175, 10, 325, 25)
button3 =pg.Rect(550, 10, 75, 25)
button4 = pg.Rect(750, 10, 75, 25)
button5 = pg.Rect(850, 10, 75, 25)
textsurface = font.render('LEFT <--                          UP               DOWN                   RIGHT           JUMP', False, (255, 255, 255))
        


pg.draw.rect(screen, [250, 0, 250], button1)  # draw button
pg.draw.rect(screen, [255, 255, 0], button2)
pg.draw.rect(screen, [0, 0, 255], button3)
pg.draw.rect(screen, [0, 255, 0], button4)
pg.draw.rect(screen, [0, 255, 255], button5)


pg.display.flip()

if button1.collidepoint(mouse_pos):
     print('button1 was pressed at {0}'.format(mouse_pos))
if button2.collidepoint(mouse_pos):
     print(button2 was pressed)
print('button2 was pressed at {0}'.format(mouse_pos))

if button3.collidepoint(mouse_pos):
# prints current location of mouse
 print('button3 was pressed at {0}'.format(mouse_pos))
if button4.collidepoint(mouse_pos):
# prints current location of mouse
 print('button4 was pressed at {0}'.format(mouse_pos))
if button5.collidepoint(mouse_pos):
# prints current location of mouse
 print('button5 was pressed at {0}'.format(mouse_pos))



'''
text5.insert(tk.END, note_str33)
notestr51 = '''
import pygame as pg



from pygame.locals import *      
import sys
 
# 1200 x 630

W = 300
H = 158
HW = W / 2
HH = H / 2


QW = HW / 4
QH = HH/  4

screen = pg.display.set_mode((1200, 800))
clock = pg.time.Clock()

bg_img = pg.image.load("gx/bg88.png") 




class Subsurf:

    def __init__(self, pos, size, image):
        self.image =image
        self.size = size
        self.pos = pos
        self.w, self.h = self.size
        self.x, self.y = self.pos
        self.make_subrect()

    def make_subrect(self):
        self.rect = pg.Rect(self.image.get_rect())
        self.sub_surf = self.image.subsurface(self.rect)
        self.surf= pg.Surface((2000, 2000))
        self.surf.blit(self.sub_surf, (HW,HH))
      
        return self.sub_surf, self.surf


##    def blit(self, sub_surf, x, y):
##        screen.blit(sub_surf, (self.x, self.y))    
##
i = 0
j = 0
 
pos = (400,800)
size = (HW, HH)

s = Subsurf(pos,size, bg_img)
ss = Subsurf(pos,size, bg_img)
ss2 = Subsurf(pos,size, bg_img)
ss3 = Subsurf(pos,size, bg_img)
#bg_img = pg.transform.scale(bg_img,(width,height))

 
loop = True
while loop:
    screen.fill((0,0,0))
##    screen.blit(bg_img,(i,j))
   
    screen.blit(bg_img,(QW, QH))
    screen.blit(s.sub_surf,(i, j))
    screen.blit(ss.sub_surf,((-i, -j)))
    screen.blit(ss2.sub_surf,(-i, j))
    screen.blit(ss2.sub_surf,(i, -j))
    for event in pg.event.get():
        if event.type == QUIT:
            loop = False
    i += 0.5
    j += 0.5
    pressed = pg.key.get_pressed()
     

    if pressed[pg.K_UP]:
        j-= 1
##        screen.blit(bg_img,(0, height+j))
      
    if pressed[pg.K_DOWN]:
        j += 1
##        screen.blit(bg_img,(0, height+j))
          
    if pressed[pg.K_LEFT]:
        i-= 5
##        screen.blit(bg_img,(width+i, 0))

    if pressed[pg.K_RIGHT]:
        i += 5
##        screen.blit(bg_img,(width + i, 0))     
    pg.display.update()
pg.quit()


'''

text6.insert(tk.END, notestr51)



notestr52 = '''
import pygame as pg
import random

pg.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

# I changed the background color to black, because I understood it as that is what you want.
BACKGROUND_COLOR = (0, 0, 0)  # tausta_vari

clock = pg.time.Clock()  # kello
star = pg.Surface((32, 32))
star.fill((255, 255, 255))

planets = random.randrange(100, 500)
positions = [(300, 50), (400, 27), (900, 55)]

WIDTH, HEIGHT = (1000, 1000)  # (leveys, korkeus)
screen = pg.display.set_mode((WIDTH, HEIGHT))  # ikkuna
pg.display.set_caption("SpaceGenerationTest")

display_stars = False
running = True  # toiminnassa
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                print("Generating World....")
                print(planets)
                display_stars = True

    screen.fill(BACKGROUND_COLOR)

    if display_stars:
        for position in positions:
            # This will create 3 stars because there're 3 elements in the list positions.
            # To create more stars you'll need to add more in the list positions.
            screen.blit(star, position)

    pg.display.update()
'''
text7.insert(END, notestr52)
notestr53 = '''import pygame as pg
import random
from pygame.locals import *
from pygame import Surface








class Constants:
   
    WHITE = ((255,255,255))
    WIDTH = 1300
    HEIGHT = 800
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    MARGINX = 325
    MARGINY = 240
    W = WIDTH
    H = HEIGHT
    HW = W / 2
    QW = W / 4
    HQW = HW + QW
    HH = H /2
    QH = H / 4
    HQH = HH + QH
    
    
class Markerrects:
    def __init__(self, position, size):
        self.position = pg.math.Vector2(position)
        self.size = pg.math.Vector2(size)
        self.x, self.y = self.position
        self.w, self.h = self.size
        self.xx = self.x * 2
        self.yy = self.y * 2
        self.w2 = self.w * 2
        self.h2 = self.h * 2
        self.hw = self.w / 2
        self.hh = self.h / 2
        self.make_inner_rect()
        self.make_outer_rect()

        def make_inner_rect():
            return pg.Rect(self.hw, self.hw, self.w, self.h)

        def make_outer_rect():
            return pg.Rect(self.w, self.h, self.w2, self.h2)




class Background():
   
    def __init__(self, position, camera):
        self.image = pg.image.load(gx/bg.png)
        self.position = pg.math.Vector2(position)
        self.px, self.py = self.position
        self.cam = pg.math.Vector2(camera)
        self.camx, self.cam.y = self.cam
        self.bgobj = []
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pg.Rect(image.get_rect())
        self.hw = self.width / 2
        self.hh = self.height / 2
      def make_subsurf(self):
        
        self.sub_surf = self.image.subsurface(self.rect)
        self.surf= pg.Surface((self.hw, self.hh)
        self.surfsub = self.surf.subsurface(self.get_newpos(self.camx, self.camy, self.width, self.height)                      
        self.surf.blit(self.sub_surf, (self.width, self.height))
        self.surf.blit(self.surfsub, self.rect)                      
                            
        
      def get_newpos(self, camx, camy, width, height):
        # create a Rect of the camera view
        #create random coordinates for background images that need to be added
        self.cam_rect = pg.Rect(self.camx, self.camy, self.width, self.height)
        while True:
           self.xsub = random.randint(self.camx - self.width * 2, self.camx + (2 * self.width))
           self.ysub = random.randint(self.camy - self.height * 2, self.camy + (2 * self.height))
            # create a Rect object with the random coordinates and use colliderect()
            # to make sure the right edge isn't in the camera view.
            self.obj_rect = pg.Rect(self.xsub, self.ysub, self.width, self.height)
            if not self.obj_rect.colliderect(self.cam_rect):
                return self.xsub, self.ysub


    

        

    
                
'''
text8.insert(END, notestr53)


notestr54 = '''

import pygame as pg

def scrollX(target_surf, source_surf, offset_x):
    width, height = target_surf.get_size()
    target_surf.blit(source_surf, (offset_x, 0))
    if offset_x < 0:
        target_surf.blit(source_surf, (width + offset_x, 0), (0, 0, -offset_x, height))
    else:
        target_surf.blit(source_surf, (0, 0), (width - offset_x, 0, offset_x, height))

def scrollY(target_surf, source_surf, offset_y):
    width, height = source_surf.get_size()
    target_surf.blit(source_surf, (0, offset_y))
    if offset_y < 0:
        target_surf.blit(source_surf, (0, height + offset_y), (0, 0, width, -offset_y))
    else:
        target_surf.blit(source_surf, (0, 0), (0, height - offset_y, width, offset_y))

pg.init()
window = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

background = pg.Surface(window.get_size())
ts, w, h, c1, c2 = 100, *window.get_size(), (64, 64, 64), (127, 64, 64)
tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
for rect, color in tiles:
    pg.draw.rect(background, color, rect)
pos_x, pos_y, speed = 0, 0, 10

run = False
while not run:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = True

    keys = pg.key.get_pressed()
    pos_x = (pos_x + (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * speed) % window.get_width()
    pos_y = (pos_y + (keys[pg.K_DOWN] - keys[pg.K_UP]) * speed) % window.get_height()

    scrollX(window, background, pos_x)
    scrollY(window, window.copy(), pos_y)

    pg.display.flip()

pg.quit()
exit()
'''
text8.insert(END, notestr54)
notestr55 = '''# Importing the pygame module
import pygame
from pygame.locals import *
 
# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()
 
# Create a display surface object
# of specific dimension
window = pygame.display.set_mode((600, 600))
 
 
# Create a list of different sprites
# that you want to use in the animation
image_sprite = [pygame.image.load("Sprite1.png"),
                pygame.image.load("Sprite2.png")]
 
 
# Creating a new clock object to
# track the amount of time
clock = pygame.time.Clock()
 
# Creating a new variable
# We will use this variable to
# iterate over the sprite list
value = 0
 
# Creating a boolean variable that
# we will use to run the while loop
run = True
 
# Creating an infinite loop
# to run our game
while run:
 
    # Setting the framerate to 3fps just
    # to see the result properly
    clock.tick(3)
 
    # Setting 0 in value variable if its
    # value is greater than the length
    # of our sprite list
    if value >= len(image_sprite):
        value = 0
 
    # Storing the sprite image in an
    # image variable
    image = image_sprite[value]
 
    # Creating a variable to store the starting
    # x and y coordinate
    x = 150
 
    # Changing the y coordinate
    # according the value stored
    # in our value variable
    if value == 0:
        y = 200
    else:
        y = 265
 
    # Displaying the image in our game window
    window.blit(image, (x, y))
 
    # Updating the display surface
    pygame.display.update()
 
    # Filling the window with black color
    window.fill((0, 0, 0))
 
    # Increasing the value of value variable by 1
    # after every iteration
    value += 1'''
notestr57= ''' class Game:
    """Just a quick game skeleton to test out the viewport."""

    def __init__(self):
        self.screen = pg.display.set_mode((800, 800))
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
##        self.world_map = WorldMap()
##        self.viewport = Viewport(self.world_map.surf)
##
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.viewport.get_event(event)

    def update(self):
##        self.world_map.update()
##        self.world_map.draw()
##        self.viewport.update(self.world_map.surf)

    def draw(self, surface):
        #surface.blist((
        self.viewport.draw(self.screen)

    def run(self):
        self.loop = True
        while self.loop:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)
            pg.display.set_caption("FPS: {}".format(self.clock.get_fps()))


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.run()
    pg.quit()
    sys_exit()

'''
f117 = ttk.Frame(notebook)
notebook.add(f117, text='117')
notebook3 = ttk.Notebook(f117)

notebook3.grid(row=2, column=2)
fffr1 = ttk.Frame(notebook3)
fffr2 = ttk.Frame(notebook3)

notebook3.add(fffr1, text='10')
notebook3.add(fffr2, text='20')

fffr3 = ttk.Frame(notebook3)
notebook3.add(fffr3, text='30')
ttextt33 = ScrolledText(fffr3, height=50, width=100, bg='wheat' ,bd=10)
ttextt33.insert('1.0', tk.END)
ttextt33.grid(row=2, column=4, rowspan=25, columnspan=10)
fffr4 = ttk.Frame(notebook3)
notebook3.add(fffr4, text='40')
fffr5 = ttk.Frame(notebook3)
        
# Combobox creation


notebook3.add(fffr5, text='50')
fffr6 = ttk.Frame(notebook3)
notebook3.add(fffr6, text='60')
fffr7 = ttk.Frame(notebook3)
notebook3.add(fffr7, text='70')
fffr8 = ttk.Frame(notebook3)
notebook3.add(fffr8, text='80')
fffr9 = ttk.Frame(notebook3)
notebook3.add(fffr9, text='90')
fffr10 = ttk.Frame(notebook3)
notebook3.add(fffr10, text='100')
fffr11 = ttk.Frame(notebook3)
notebook3.add(fffr11, text='110')
fffr12 = ttk.Frame(notebook3)
notebook3.add(fffr12, text='120')
fffr13 = ttk.Frame(notebook3)
notebook3.add(fffr13, text='130')
fffr14 = ttk.Frame(notebook3)
notebook3.add(fffr14, text='140')
fffr15 = ttk.Frame(notebook3)
notebook3.add(fffr15, text='150')
ff116 = ttk.Frame(notebook3)
notebook3.add(ff116, text='1160')

ttextt10 = ScrolledText(f10, height=50, width=100, bg='wheat', bd=10)
ttextt10.insert('1.0', tk.END)
ttextt10.grid(row=0, column=4, rowspan=25, columnspan=10)

ttextt4 = ScrolledText(f4, height=50, width=300, bg='wheat', bd=10)
ttextt4.insert('1.0', tk.END)

ttextt4.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt5 = ScrolledText(f5, height=50, width=300, bg='white',bd=10)
ttextt5.insert('1.0', tk.END)
ttextt5.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt6 = ScrolledText(f6, height=50, width=100, bg='white',bd=10)
ttextt6.insert('1.0', tk.END)
ttextt6.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt7 = ScrolledText(f7, height=50, width=100, bg='light blue',bd=10)
ttextt7.insert('1.0', tk.END)
ttextt7.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt8 = ScrolledText(f8, height=50, width=100, bg='pink')
ttextt8.insert('1.0', tk.END)
ttextt8.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt9 = ScrolledText(f9, height=50, width=100, bg='light green', bd=10)
ttextt9.insert('1.0', tk.END)
ttextt9.grid(row=0, column=4, rowspan=25, columnspan=10)


ttextt11 = ScrolledText(f11, height=50, width=100, bg='wheat',bd=10)
ttextt11.insert('1.0', tk.END)
ttextt11.grid(row=0, column=4, rowspan=25, columnspan=10)

ttextt12 = ScrolledText(f12, height=50, width=300, bg='wheat',bd=10)
ttextt12.insert('1.0', tk.END)

ttextt12.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt13 = ScrolledText(f13, height=50, width=300, bg='white', bd=10)
ttextt13.insert('1.0', tk.END)
ttextt13.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt14 = ScrolledText(f14, height=50, width=100, bg='white', bd=10)
ttextt14.insert('1.0', tk.END)
ttextt14.grid(row=0, column=4, rowspan=25, columnspan=10)
ttextt15 = ScrolledText(f15, height=50, width=100, bg='light blue', bd=10)
ttextt15.insert('1.0', tk.END)
ttextt15.grid(row=0, column=4, rowspan=25, columnspan=10)



fr_btn2 = tk.Frame(f10, relief=tk.RAISED, bd=6)
btnn_open = tk.Button(fr_btn2, text='Open',bd=6,  command= lambda:open_file(ttextt10, f10))
btnn_save = tk.Button(fr_btn2, text='Save As...', bd=6, command= lambda:save_file(ttextt10, f10))
def ggttxt2():
    a = text2.get("1.0", tk.END)
    ttxt_edit.insert(tk.END, a)

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)
btnn_grab =tk.Button(fr_btn2, text='Grab from F1...', bd=6,  command= lambda: ggttxt(ttextt10, f10))
btnn_grab.grid(row=2, column=0)
fr_btn2.grid(row=0, column=0, sticky='ns')


fr_btn3 = tk.Frame(f4, relief=tk.RAISED, bd=6)
btnn_open = tk.Button(fr_btn3, text='Open', bd=6, command= lambda:open_file(ttextt4, f4))
btnn_save = tk.Button(fr_btn3, text='Save As...', bd=6, command= lambda:save_file(ttextt4, f4))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn3.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(f5, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt5, f5))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt5, f5))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(f6, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt6, f6))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt6, f6))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(f7, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt7, f7))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt7, f7))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(f8, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt8, f8))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt8, f8))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(f9, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt9, f9))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt9, f9))



fr_btn = tk.Frame(f11, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt11, f11))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt11, f11))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(f12, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt12, f12))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt12, f12))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(f13, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt13, f13))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt13, f13))
btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(f4, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttextt15, f15))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttextt15, f15))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')


ttxt1 = ScrolledText(fffr1, height=50, width=300, bg='wheat')
ttxt1.insert('1.0', tk.END)
ttxt2= ScrolledText(fffr2, height=50, width=300, bg='wheat')
ttxt2.insert('1.0', tk.END)
ttxt3 = ScrolledText(fffr4, height=50, width=300, bg='wheat')
ttxt3.insert('1.0', tk.END)
ttxt4 = ScrolledText(fffr4, height=50, width=300, bg='wheat')
ttxt4.insert('1.0', tk.END)


ttxt4.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt5 = ScrolledText(fffr5, height=50, width=300, bg='white')
ttxt5.insert('1.0', tk.END)
ttxt5.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt6 = ScrolledText(fffr6, height=50, width=100, bg='white')
ttxt6.insert('1.0', tk.END)
ttxt6.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt7 = ScrolledText(fffr7, height=50, width=100, bg='light blue')
ttxt7.insert('1.0', tk.END)
ttxt7.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt8 = ScrolledText(fffr8, height=50, width=100, bg='pink')
ttxt8.insert('1.0', tk.END)
ttxt8.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt9 = ScrolledText(fffr9, height=50, width=100, bg='light green')
ttxt9.insert('1.0', tk.END)
ttxt9.grid(row=0, column=4, rowspan=25, columnspan=10)

ttxt10 = ScrolledText(fffr10, height=50, width=300, bg='wheat')
ttxt10.insert('1.0', tk.END)

ttxt10.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt11 = ScrolledText(fffr11, height=50, width=300, bg='white')
ttxt11.insert('1.0', tk.END)
ttxt11.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt12 = ScrolledText(fffr12, height=50, width=100, bg='white')
ttxt12.insert('1.0', tk.END)
ttxt12.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt13 = ScrolledText(fffr13, height=50, width=100, bg='light blue')
ttxt13.insert('1.0', tk.END)
ttxt13.grid(row=0, column=4, rowspan=25, columnspan=10)
ttxt14 = ScrolledText(fffr14, height=50, width=100, bg='pink')
ttxt14.insert('1.0', tk.END)
ttxt14.grid(row=0, column=4, rowspan=25, columnspan=10)
fr_btn = tk.Frame(fffr1, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt1, fffr1))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt1, fffr1))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')
ttxt1.grid(row=0, column=1, sticky='nsew')


fr_btn = tk.Frame(fffr2, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt2, fffr2))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt2, fffr2))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')
ttxt2.grid(row=0, column=1, sticky='nsew')



fr_btn = tk.Frame(fffr3, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt3, fffr3))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt3, fffr3))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(fffr4, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt4, fffr4))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt4, fffr4))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(fffr5, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt5, fffr5))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt5, fffr5))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(fffr6, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt6, fffr6))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt6, fffr6))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(fffr7, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt7, fffr7))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt7, fffr7))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')



fr_btn = tk.Frame(fffr8, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt8, fffr8))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt8, fffr8))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(fffr9, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt9, fffr9))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt9, fffr9))

btnn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btnn_save.grid(row=1, column=0, sticky='ew', padx=5)

fr_btn.grid(row=0, column=0, sticky='ns')




fr_btn = tk.Frame(fffr10, relief=tk.RAISED, bd=2)
btnn_open = tk.Button(fr_btn, text='Open',  command= lambda:open_file(ttxt10, fffr10))
btnn_save = tk.Button(fr_btn, text='Save As...',  command= lambda:save_file(ttxt10, fffr10))



root.mainloop()
