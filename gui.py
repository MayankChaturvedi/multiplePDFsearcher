from tkinter import *
import PyPDF2
import re
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)
def goforit(a,String):
    # open the pdf file
    object = PyPDF2.PdfFileReader(a)

    # get number of pages
    NumPages = object.getNumPages()

    # define keyterms

    # extract text and do the search
    cnt=0
    foc=-1
    for i in range(0, NumPages):
        PageObj = object.getPage(i)
        Text = PageObj.extractText()
        if re.search(String, Text, re.IGNORECASE):
            if cnt==0:
                foc=i
            cnt+=1
    ret=[]
    if cnt!=0:
        ret.append("😍 found "+String+" in the pdf - "+str(a)+" goto page number "+str(foc)+"\n( "+str(cnt)+" occurances )\n")
        ret.append("in file "+str(a)+" word "+String+" seen in "+str(cnt)+" pages first occurance in page "+str(foc))
    else:
        ret.append("Oh no! 🥴 no occurance of your word found\n")
    return ret

def fun(tString):
    tString
    for a in files:
        lst=goforit(a,tString)
        for b in lst:
            print(b)


window = Tk()

window.title("Made with ♥️ for math peeps")

window.geometry('500x450')

lbl = Label(window, text="the word you want to search : ")

lbl.grid(column=0, row=0)

txt = Entry(window,width=10)

txt.grid(column=1, row=0)

lbl2=Label(window,text="searching... ")	

def solveqry(a):
    fun(a)
    lbl2.configure(text="search sucessful")

def clicked():
    lbl2.configure(text="searching... ")
    lbl2.grid(column=6,row=0)
    output=solveqry(txt.get())
    

btn = Button(window, text=" Go ", command=clicked)

btn.grid(column=2, row=0)

window.mainloop()
