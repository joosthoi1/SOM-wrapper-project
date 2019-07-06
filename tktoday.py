import somapi
import json
import tkinter as tk
from functools import partial
from tkinter import messagebox
import os
from onvoldoende_hulp import calculateOnvoldoende

'bcc500b0-8f13-458a-857c-c17ee6531c61'
class login:
    def __init__(self):
        self.root = tk.Tk()

        self.schools = somapi.Sapi().get_schools()
        namen = ['{} - {}'.format(i['naam'], i['plaats']) for i in self.schools]
        width = (max([len(i) for i in namen]))
        namen.sort()
        tk.Label(self.root,text='school: ').grid(row=0,column=0,sticky='nw')
        tk.Label(
            self.root,text='gebruikersnaam: '
        ).grid(row=1,column=0,sticky='w')
        tk.Label(self.root,text='wachtwoord: ').grid(row=2,column=0,sticky='w')

        self.listbox = tk.Listbox(self.root,
            selectmode=tk.BROWSE,
            width=width,
            font=("Helvetica", 9),
            exportselection=0
        )

        for i in namen:
            self.listbox.insert(tk.END, i)

        self.listbox.grid(row=0,column=1)

        scrollbar = tk.Scrollbar(self.root, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.grid(row=0,column=2,sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)
        username = tk.Entry(self.root, width=width, font=("Helvetica", 9))
        username.grid(row=1,column=1)
        password = tk.Entry(
            self.root,
            width=width,
            show='*',
            font=("Helvetica", 9))
        password.grid(row=2,column=1)
        button = tk.Button(self.root, text='Done', command = partial(
            self.login, self.listbox, username, password
            ))
        button.grid(row=3,column=1,sticky='e')
        self.root.bind_all('<Return>', lambda event: button.invoke())
        self.root.mainloop()
        return

    def login(self, school, username, password):
        username = username.get()
        password = password.get()
        if not username:
            tk.messagebox.showerror(
            'Error',
            'Geen gebruikersnaam ingevult')
            return
        elif not password:
            tk.messagebox.showerror(
            'Error',
            'Geen wachtwoord ingevult')
            return
        elif not school.curselection():
            tk.messagebox.showerror(
            'Error',
            'Geen school geselecteerd')
            return

        school = school.get(school.curselection()[0]).split(' - ')[0]
        for i in self.schools:
            if i['naam'] == school:
                uuid = i['uuid']
        s = somapi.Sapi()
        try:
            s.get_auth(uuid, username, password)
        except somapi.AuthenticateError as e:

            msg = json.loads(e.__str__().replace('\'','\"'))
            if hasattr(self, 'error'):
                self.error.destroy()
            self.error = tk.Label(
            self.root,
                text=msg['error_description'],
            )
            self.error.grid(row=3,column=1,sticky='w')
            tk.messagebox.showerror(
                'Error',
                'Gebruikersnaam of wachtwoord onjuist')
            return
        self.root.destroy()

class cijfers:
    def __init__(self):
        s = somapi.Sapi()
        s.get_auth()
        id = s.get_id()[0]['id']
        self.grades = s.get_grades(id)
#        print(json.dumps(self.grades, indent=4))
        self.root = tk.Tk()
        self.add_scrollbar()
        self.root.mainloop()

    def add_scrollbar(self):
        self.canvas = tk.Canvas(
            self.root,
            borderwidth=0,
            background="#ffffff",
            height=1000
        )
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (4,4), window=self.frame, anchor="nw",
            tags="self.frame"
        )

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.populate()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def populate(self):
        '''Put in some fake data'''
        for row, i in enumerate(self.grades[::-1]):
            if i['type'] == 'Toetskolom':
                f = tk.Frame(self.frame,borderwidth=3, relief='sunken')
                f.pack(anchor='w', fill='x')
                tk.Label(f, text=i['vak']).grid(row=0, column=0, sticky='w')
                for1 = ' {} '.format(i['omschrijving'])
                if 'resultaat' in i:
                    for2 = i['resultaat']
                else:
                    for2 = i['resultaatLabelAfkorting']

                t = 'Je hebt voor de toets{}een {} gehaalt'.format(for1,for2)

                tk.Label(
                    f,
                    text=t,
                    wraplength=370,
                    justify='left'
                ).grid(row=1, column=0, sticky='w')

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



class test:
    def __init__(self):
        s = somapi.Sapi()
        s.get_schools()
        s.get_auth()
        id = s.get_id()[0]['id']
        self.grades = s.get_grades(id)
#        print(json.dumps(self.grades, indent=4))
        self.group_by_type()
        self.root = tk.Tk()
        self.root.title('TkToday')
        self.add_scrollbar()
        self.root.mainloop()


    def add_scrollbar(self):
        self.canvas = tk.Canvas(
            self.root,
            borderwidth=0,
            background="#ffffff",
            height=500
        )
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (4,4),
            window=self.frame,
            anchor="nw",
            tags="self.frame"
        )

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.populate()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def open_grades(self, vak):
        if not self.is_open[vak]:
            periodelijst = []
            self.open_frames[vak] = tk.Frame(self.framelist[vak])
            self.open_frames[vak].grid(row=2,column=0,sticky='w')

            gemmidelde_periode = ['']*4
            for i in self.lijst[vak]:
                if i['type'] == 'RapportGemiddeldeKolom':
                    if 'geldendResultaat' in i:
                        gemmidelde_periode[i['periode']-1] = i[
                            'geldendResultaat'
                        ]
                    elif 'resultaatLabelAfkorting' in i:
                        gemmidelde_periode[i['periode']-1] = i[
                            'resultaatLabelAfkorting'
                        ]
                    else:
                        gemmidelde_periode[i['periode']-1] = '-'
            for i in range(4):
                text = f'Periode {i+1}'.ljust(90) + str(
                    gemmidelde_periode[i]
                )
                periodelijst.append(
                    tk.LabelFrame(self.open_frames[vak],text = text)
                    )
                periodelijst[-1].pack(anchor='w')
            for row, i in enumerate(self.lijst[vak]):
                self.root.update()
                cond1 = not i['isExamendossierResultaat']
                cond = 'geldendResultaat' in i or 'resultaatLabelAfkorting' in i
                if i['type'] == 'Toetskolom' and cond1 and cond:
                    if 'geldendResultaat' in i:
                        cijfer = float(i['geldendResultaat'])
                    elif 'resultaatLabelAfkorting' in i:
                        cijfer = i['resultaatLabelAfkorting']

                    if type(cijfer) == float and cijfer < 6:
                        color = 'OrangeRed2'
                    elif cijfer == 'O':
                        color = 'OrangeRed2'
                    else:
                        color = None

                    text = '{}'.format(i['omschrijving'])
                    text_weging = '   ({})'.format(i['weging'])

                    tk.Label(
                        periodelijst[i['periode']-1],
                        text = text,
                        wraplength=335,
                        justify='left',
                        anchor='w',
                        relief='raised',
                        bd=1,
                        width=45
                        ).grid(row=row, column=0, sticky='w')

                    tk.Label(
                        periodelijst[i['periode']-1],
                        text = cijfer,
                        font = ('Calibiri', 9, 'bold'),
                        fg = color,
                        ).grid(row=row, column=1, sticky='nw')

                    tk.Label(
                        periodelijst[i['periode']-1],
                        text = text_weging,
                        ).grid(row=row, column=2, sticky='nw')

            self.is_open[vak] = True
        else:
            for i in self.open_frames[vak].winfo_children()[::-1]:
                i.destroy()
                self.root.update()
            self.open_frames[vak].destroy()
            self.is_open[vak] = False

    def onvoldoende(self, vak):
        cijferlijst = []
        for i in self.lijst[vak]:
            condition = 'geldendResultaat' in i
            if i['type'] == 'Toetskolom' and not i['teltNietmee'] and condition:
                cijferlijst.append((i['geldendResultaat'], i['weging']))
        if cijferlijst:
            root = tk.Toplevel()
            calculateOnvoldoende(root, cijferlijst)
            root.mainloop()

    def populate(self):
        '''Put in some fake data'''
        self.framelist = {}
        for row, i in enumerate(self.vakkenlijst):
            tk.Frame(self.frame,height=1,bg='#3399ff').pack(fill='x')
            self.framelist[i] = tk.Frame(
                self.frame,
                relief = 'flat',
                bd=1,
                bg=None
            )
            self.framelist[i].pack(anchor='w',fill='x')
            b = tk.Button(
                self.framelist[i],
                command = partial(self.open_grades, i),
                text=i,
                anchor = 'w',
                bg='ghost white',
                fg='#3399ff',
                font=('Calibiri', 10),
                width=46,
                height=1
                )
            b.grid(row=0,column=0,sticky='w')
            for x in self.lijst[i]:
#                print(x['type'], x['periode'], x['vak'])
                if x['type'] == "RapportGemiddeldeKolom" and x['periode'] == 4:
                    if 'geldendResultaat' in x:
                        if x['geldendResultaat'][0].isdigit():
                            cijfergemmidelde = round(
                                float(x['geldendResultaat'])
                                )
                        else:
                            cijfergemmidelde = x['geldendResultaat']

                    elif 'resultaatLabelAfkorting' in x:
                        cijfergemmidelde = x['resultaatLabelAfkorting']

                if x['type'] == "SEGemiddeldeKolom" and x['periode'] == 0:
                    if 'geldendResultaat' in x:
                        se_cijfergemmidelde = x['geldendResultaat']

                    elif 'resultaatLabelAfkorting' in x:
                        se_cijfergemmidelde = x['resultaatLabelAfkorting']

            for q in self.lijst[i][::-1]:
                if x['type'] == "Toetskolom":
                    if 'geldendResultaat' in x:
                        nieuwste_cijfer = x['geldendResultaat']
                        break
                    elif 'resultaatLabelAfkorting' in x:
                        nieuwste_cijfer = x['resultaatLabelAfkorting']
                        break

            if not 'nieuwste_cijfer' in locals():
                nieuwste_cijfer = None
            if not 'cijfergemmidelde' in locals():
                cijfergemmidelde = '-'
            if not 'se_cijfergemmidelde' in locals():
                se_cijfergemmidelde = '-'

            if type(cijfergemmidelde) == int and cijfergemmidelde < 6:
                color = 'OrangeRed2'
            else:
                color = None

            if type(se_cijfergemmidelde) == int and se_cijfergemmidelde < 6:
                color_se = 'OrangeRed2'
            else:
                color_se = None

            if type(nieuwste_cijfer) == int and cijfergemmidelde < 6:
                color_nieuw = 'OrangeRed2'
            else:
                color_nieuw = None

            f2 = tk.Frame(self.framelist[i], height=30,width=378)
            f2.grid(row=1, column=0,sticky='w')
            f2.pack_propagate(0)

            tk.Label(f2, text= 'R4:  ',bg=None,).pack(side='left')
            tk.Label(
                f2,
                text=cijfergemmidelde,
                fg = color,
                font=('Calibiri', 9, 'bold'),
                bg=None
                ).pack(side='left')
            tk.Label(f2, text= '  SE: ',bg=None).pack(side='left')
            tk.Label(
                f2,
                text=se_cijfergemmidelde,
                fg = color_se,
                font=('Calibiri', 9, 'bold'),
                bg=None
                ).pack(side='left')
            if not nieuwste_cijfer:
                nieuwste_cijfer = '  - '
            tk.Label(
                f2, text= '  Nieuwste cijfer: ',
                bg=None
                ).pack(side='left')
            tk.Label(
                f2,
                text=nieuwste_cijfer,
                fg = color_nieuw,
                font=('Calibiri', 9, 'bold'),
                bg=None
                ).pack(side='left')
            tk.Button(
                f2,
                command = partial(self.onvoldoende, i),
                text = 'Onvoldoende Hulp'
                ).pack(side='right',anchor='e')

            del cijfergemmidelde, nieuwste_cijfer, se_cijfergemmidelde


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def group_by_type(self):
        self.lijst = {}
        self.typelijst = []
        for i in self.grades:
                if not i['type'] in self.typelijst:
                    self.typelijst.append(i['type'])
#            if i['type'] == 'Toetskolom':
                if not i['vak'] in self.lijst:
                    self.lijst[i['vak']] = []
                self.lijst[i['vak']].append(i)
        self.vakkenlijst = list(self.lijst.keys())
        self.is_open = {}
        self.open_frames = {}
        for i in self.vakkenlijst:
            self.is_open[i] = False
#                if 'geldendResultaat' in i:
#                    lijst[i['vak']].append(i['geldendResultaat'])
#                elif 'resultaatLabelAfkorting' in i:
#                    lijst[i['vak']].append(i['resultaatLabelAfkorting'])
#        print(json.dumps(self.lijst, indent=4))
#        print(self.typelijst, '\n', self.vakkenlijst)
#        print([len(i) for i in lijst.values()])
#        print(sum([len(i) for i in self.lijst.values()]))
if __name__ == '__main__':
    if not os.path.isfile('token.json'):
        login()
    test()
#    login()
