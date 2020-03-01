from tkinter import *
import PyPDF2
import re
import webbrowser
import os, sys, subprocess

class DoubleScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = Scrollbar(self.outer, orient=HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            func(1, "units" )



def callback(url):
    webbrowser.open_new(url)
tot=0
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
    global tot
    tot=(cnt+(tot))
    ret=[]
    if cnt!=0:
        ret.append(":) found "+String+" in the pdf - "+str(a)+" goto page number "+str(foc)+"\n( "+str(cnt)+" occurances )\n")
    return ret


    

root = Tk()
root.geometry("900x800")

root.title("Made with :) for math peeps")

up = Frame(root, borderwidth=2, relief="solid")

up.pack(side="top", expand=True, fill="both")

uplft=Frame(up,width=50)

uplft.pack(side="left")

upcent=Frame(up,width=50)

upcent.pack(side="left")

uprgt=Frame(up,width=50)

uprgt.pack(side="left")

lbl = Label(uplft, text="the word you want to search : ",font=("Courier", 18))

lbl.pack()

txt = Entry(upcent,width=25)

txt.pack()

lbl2=Label(up,text="")
lbl2.pack(side="right")

dfrm=DoubleScrolledFrame(root,height=20, width=1000, borderwidth=2, relief=SUNKEN, background="light gray")
dfrm.pack(side="bottom", expand=True)




scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)
 
area = Text(root, yscrollcommand = scrollbar.set,font="Calibri 16")

area.pack(expand=True, fill='both')

scrollbar.config(command = area.yview)

def open(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
        
blst=[]
def fun(tString):
    area.delete('1.0', END)
    for btn in blst:
        btn.destroy()
    blst.clear()
    dfrm.pack(side="bottom", expand=True)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)
    tString
    global tot
    tot=0
    tt=1
    opfiles=[]
    for a in files:
        lst=goforit(a,tString)
        for b in lst:
            area.insert(END,b+'\n')
            opfiles.append(str(a))
    if tot==0:
        area.insert(END," :( Ah shit! Here we go again. The word not found")
    else:
        for i in range(0,len(opfiles)):
            button = Button(dfrm,text=opfiles[i], command=lambda i=i: open(opfiles[i]))
            button.pack(side="left")
            blst.append(button)
            
def solveqry(a):
    fun(a)
    lbl2.configure(text="search sucessful")

def clicked():
    solveqry(txt.get())

btn = Button(uprgt, text=" Go ", command=clicked)

btn.pack()

root.mainloop()
