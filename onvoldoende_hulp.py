import tkinter as tk
from tkinter import messagebox

class calculateOnvoldoende:
    def __init__(self, root, prefilled=None):
        self.topframe = tk.Frame(root)
        self.topframe.pack(side='top', fill="x")
        self.bottomframe = tk.Frame(root)
        self.frame = tk.Frame(root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.bottomframe.pack(side='top', fill='x')
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.row = 0
        self.rijen = []
        self.wegingen = []
        self.cijfers = []

        self.populate()
        if prefilled:
            for i in prefilled:
                self.addline(i)
        else:
            self.addline()

    def populate(self):
        tk.Label(self.topframe, text='Wat wil je minimaal staan?'.ljust(30)).grid(row=0,column=0)
        self.minimaal = tk.Entry(self.topframe, width=4)
        self.minimaal.grid(row=0,column=1)
        tk.Label(self.topframe, text='Weging komende toets'.ljust(30)).grid(row=1,column=0)
        self.weging = tk.Entry(self.topframe, width=4)
        self.weging.grid(row=1,column=1)
        tk.Button(self.bottomframe, command=self.addline,text='add line').pack(side='left')
        tk.Button(self.bottomframe, command=self.removeline,text='remove line').pack(side='left')
        tk.Button(self.bottomframe, command=self.math,text='calculate').pack(side='left')
        tk.Label(self.frame, text='#  ').grid(row=0,column=0)
        tk.Label(self.frame, text='Cijfer').grid(row=0,column=1)
        tk.Label(self.frame, text='Weging').grid(row=0,column=2)

    def addline(self, text=None):
        if text:
            cijfer = str(text[0])
            weging = str(text[1])

        self.rijen.append(tk.Label(self.frame, text=self.row+1))
        self.rijen[self.row].grid(row=self.row+1,column=0)

        self.cijfers.append(tk.Entry(self.frame, width=4))
        self.cijfers[self.row].grid(row=self.row+1,column=1)
        if text:
            self.cijfers[self.row].insert(0,cijfer)

        self.wegingen.append(tk.Entry(self.frame, width=4))
        self.wegingen[self.row].grid(row=self.row+1, column=2)
        if text:
            self.wegingen[self.row].insert(0,weging)
        self.row += 1

    def removeline(self):
        if self.rijen:
            self.rijen[-1].destroy()
            self.cijfers[-1].destroy()
            self.wegingen[-1].destroy()
            self.rijen.pop()
            self.cijfers.pop()
            self.wegingen.pop()
            self.row -= 1
    def math(self):
        if not self.weging.get() or not self.minimaal.get():
            tk.messagebox.showerror('error', 'please fill in')
            return
        alist = []
        for c,i in enumerate(self.cijfers):
            if i.get() and self.wegingen[c].get():
                weging = float(self.wegingen[c].get().replace(',','.'))
                alist.append(float(i.get().replace(',','.'))*weging)
        weging = float(self.weging.get().replace(',','.'))
        minimaal = float(self.minimaal.get().replace(',','.'))
        wegingen = [float(i.get().replace(',','.')) for i in self.wegingen if i.get()]
        te_halen = (minimaal*(weging+sum(wegingen))-sum(alist))/weging
        tk.messagebox.showinfo('cijfer', f'je moet een {round(te_halen, 2)} halen om een {minimaal} te staan')


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    alist1 = [(5,2),(6,1),(7,2),(4.9,1)]
    calculateOnvoldoende(root, alist1)
    root.mainloop()
