# -- encode utf-8 --
"""
CARDDB Handler - Une étude Python POO pour la saisie des données des types de cartes 
'creature', 'equipement' et 'spell' du jeu CARDDB en mode graphique (TKinter).
Copyright (c) 2026 Jan AMOUROUX - étude moteur du jeu
Copyright (C) 2026 Bernard AMOUROUX - étude Tkinter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

CARDDB Handler (c) 2026 Bernard AMOUROUX
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Bernard AMOUROUX"
__date__ = "$Date: 2026/08/01 07:00 $"
__copyright__ = "Copyright (c) 2026 Bernard AMOUROUX"
__license__ = "GPL 3"

import locale
import os, sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path as osp

from cardLogics import readRules
from tkinter.font import Font


class My_LabelFrame(tk.LabelFrame):

    def __init__(self,master,col=0,row=0,cspan=1,rspan=1,pad=(0,0,0,0),sticky='nsew', *args, **kwargs):

        tab_options:dict = {'bg':'ivory', 'bd':3, 'relief':'groove', 'labelanchor':'n'}
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)

        tk.LabelFrame.__init__(self,master,*args,**kwargs)        

        self.grid(column=col, row=row, columnspan=cspan, rowspan=rspan,
                                  padx=pad[0], pady=pad[1], ipadx=pad[2], ipady=pad[3], sticky=sticky)
        self.columnconfigure(list(range(cspan)), weight=1)
        self.rowconfigure(list(range(rspan)), weight=1)

    def name(self):
        return f"{self.master}."+self._name
        

class Win_MessageBox(tk.Toplevel):
    
    def __init__(self, master:tk.Tk, message:str=None, msgtext=('Consolas 11 bold italic'), *args, **kwargs):
        
        self.__master = master
        self.__name__ = 'win_messagebox'
        self.__vmessage = tk.StringVar(value=message)
        
        tab_options:dict = {'bd':3, 'bg':'wheat', 'relief':'ridge', 'pady':5}        
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)
        super().__init__(master, *args, **kwargs)
        
        self.protocol("WM_DELETE_WINDOW", self.Quit)
        self.wm_attributes("-topmost", 1)                     # - Fenetre popup toujours au premier plan
        self.resizable(False, False)
        self.grid_anchor('center')
        
        self.messageBox = tk.Message(self,bg='wheat',width=450,aspect=100,justify=tk.CENTER,
                                                        font=msgtext,textvariable=self.__vmessage)
        self.messageBox.grid(column=0,row=0,padx=20,pady=10,sticky="nsew")
        tk.Button(self,width = 8,bg='tan',text='Ok',command=self.Quit).grid(column=0,row=1,sticky="n")
        self.bind('<Return>', self.Quit)
        self.withdraw()
    
    @property
    def message(self)->str:
        return self.__vmessage.get()
    
    @message.setter
    def message(self, message):
        self.__vmessage.set(message)
        if not self.winfo_ismapped():
            self.deiconify()
            self.grab_set()
            self.lift()
        self.update()
    
    def message_update(self, message:str=""):
        self.__vmessage.set(message)
        self.update()        
    
    def textfont(self, msgtext:str):
        self.messageBox.configure(font=msgtext)
        
    def boxtitle(self, title:str):
        self.title(title)    
    
    def Quit(self, event=None):
        self.boxtitle(" Message ")
        self.grab_release()
        self.withdraw()    
   

class Application(tk.Tk):
    
    def __init__(self):
        
        tk.Tk.__init__(self, className = "Tk", useTk = True)
        
        
        self.ttlfont = Font(self, family='Courier',size=14,weight='bold',slant='italic')
        self.lblfont = Font(self, family='Consolas',size=10,weight='bold',slant='italic')
        self.itemfont= Font(self, family='Courier New',size=12,weight='bold',slant='italic')
        self.cmbfont = Font(self, family='Consolas',size=16,weight='normal',slant='italic')
        self.frmfont = Font(self, family="Times", size=12, weight="bold", slant="roman")
        
        # ---------------------------------------------------------------------
        self.protocol('WM_DELETE_WINDOW',self.Quit)
        # ---------------------------------------------------------------------
        self.columnconfigure(list(range(20)), minsize=40, weight=1)
        self.rowconfigure(list(range(1,20)), minsize=28, weight=1)
        self.rowconfigure(0, minsize=28, weight=0)
        self.minsize(width=800, height=560)
        
        self.init_variables()
        self.cree_widgets()
    
    def init_variables(self):
        self.cardtypelist:list = ["creature", "equipement", "spell"]
        self.vcardtype = tk.StringVar(value=self.cardtypelist[0])
        self.itemtypelist:list = ["arme",]
        self.vitemtype = tk.StringVar(value=self.itemtypelist[0])
        self.typesortlist:list = readRules('sort')
        self.vtypesort = tk.StringVar(value=self.typesortlist[0])

        self.armeslist = readRules('armes')
        self.vamres = tk.StringVar(value=self.armeslist[0])
        self.elementslist = readRules('elements')
        self.velements = tk.StringVar(value=self.elementslist[0])
        self.monnaielist = readRules('monnaie')
        self.vmonnaie = tk.StringVar(value=self.monnaielist[0])
        self.raceslist = readRules('races')
        self.vraces = tk.StringVar(value=self.raceslist[0])
        # ---------------------------------------------------------------------
        self.vname = tk.StringVar()
        # ---------------------------------------------------------------------
    
    def cree_widgets(self):
        globalframe = My_LabelFrame(self,cspan=20,rspan=20,pad=(2,2,2,2),sticky="nsew")
        # ---------------------------------------------------------------------
        titleframe = My_LabelFrame(globalframe,col=3,row=0,cspan=14,bg="#FBE6C8",pad=(2,2,0,0),sticky="ew")
        tk.Label(titleframe,text=" Type de carte à créer :",bg=titleframe.cget('bg'),
                                              font=self.ttlfont).grid(columnspan=6,sticky="new")
        self.comboxCardType = ttk.Combobox(titleframe,background=titleframe.cget('bg'),
                                        font=self.cmbfont,postcommand=None,values=self.cardtypelist,
                                             state="readonly",name="!comboxCardType",textvariable=self.vcardtype)
        self.comboxCardType.bind("<<ComboboxSelected>>",self.specificFrame)
        self.comboxCardType.grid(column=6,row=0,columnspan=8,sticky="new")
        # ---------------------------------------------------------------------
        self.cardtypeFrame = My_LabelFrame(globalframe,col=0,row=1,cspan=20,rspan=19,pad=(2,2,10,10))
        tk.Label(self.cardtypeFrame,text="Type de carte : ",
                               font=self.itemfont).grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="new")
        tk.Label(self.cardtypeFrame,textvariable=self.vcardtype,width=16,
                      font=self.itemfont,state="disabled").grid(row=0,column=2,columnspan=4,pady=10,sticky="nw")
        tk.Label(self.cardtypeFrame,text=" Nom du personnage :",bg=self.cardtypeFrame.cget('bg'),
                            anchor="w",font=self.itemfont).grid(row=0,column=8,columnspan=4,pady=10,sticky="ne")
        tk.Entry(self.cardtypeFrame,bg='ivory',textvariable=self.vname,
                                                   font=self.itemfont).grid(column=12,row=0,pady=10,sticky="new")
        # ---------- frame des attributs communs à toutes les carte -----------
        
        
        # ---------- frame des attributs spécifiques à Equipement -----------
        self.equipementFrame = My_LabelFrame(self.cardtypeFrame,col=0,row=18,cspan=20,bg="#E9FAD8",name="!equipementFrame",sticky="sew")
        tk.Label(self.equipementFrame,anchor="w",bg=self.equipementFrame.cget('bg'),text=" Type d'équipement :",
                                                    font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="ew")
        self.equipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                        font=self.cmbfont,postcommand=None,values=self.itemtypelist,
                                             state="readonly",name="!equipementCombobox",textvariable=self.vitemtype)
        self.equipCombobox.grid(column=2,row=0,columnspan=4,sticky="ew")
        # -------------- frame des attributs spécifiques à Sort ---------------
        self.spellFrame = My_LabelFrame(self.cardtypeFrame,col=0,row=18,cspan=20,bg="#D8E6FA",name="!spellFrame",sticky="sew")
        tk.Label(self.spellFrame,anchor="w",bg=self.spellFrame.cget('bg'),text=" Type de sort :",
                                              font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="ew")
        self.spellCombobox = ttk.Combobox(self.spellFrame,background=self.spellFrame.cget('bg'),
                                        font=self.cmbfont,postcommand=None,values=self.typesortlist,
                                             state="readonly",name="!spellCombobox",textvariable=self.vtypesort)
        self.spellCombobox.grid(column=2,row=0,columnspan=4,sticky="ew")
        # ---------------------------------------------------------------------
        self.framelist = set({self.equipementFrame,self.spellFrame})
        self.comboxCardType.event_generate("<<ComboboxSelected>>")
        # ---------------------------------------------------------------------

    def specificFrame_old(self, event:tk.Event=None):
        w = event.widget if event else self.comboxCardType
        if w.get() != "creature":
            for remove_frame in set(filter(lambda lf: w.get() not in lf.name(), self.framelist)):
                print(f"frame removed: {remove_frame.name()}")
                remove_frame.grid_remove() 
                # -------------------------------------------------------------
                grid_frame = list(self.framelist - set({remove_frame}))
                #if grid_frame:
                grid_frame = grid_frame[0]
                label = f" Attribut spécifique au type de carte '{w.get()}'"
                grid_frame.configure(bg="#E9FAD8",text=label,font=self.frmfont)
                print(f"frame grid: {grid_frame.name()} - w.get(): {w.get()}")
                grid_frame.grid()
        else:
            [frame.grid_remove() for frame in self.framelist]        
             

    def specificFrame(self, event:tk.Event=None):
        colordico:dict = {"equipement":"#E9FAD8","spell":"#D8E6FA"}
        w = event.widget if event else self.comboxCardType
        if w.get() != "creature":
            for remove_frame in set(filter(lambda lf: w.get() not in lf.name(), self.framelist)):
                print(f"frame removed: {remove_frame.name()}")
                remove_frame.grid_remove() 
                # -------------------------------------------------------------
            for grid_frame in (self.framelist - set({remove_frame})):
                label = f" Attribut spécifique au type de carte '{w.get()}'"
                grid_frame.configure(bg=colordico[w.get()],text=label,font=self.frmfont)
                print(f"frame grid: {grid_frame.name()} - w.get(): {w.get()}")
                grid_frame.grid()
        else:
            [frame.grid_remove() for frame in self.framelist]        
             
        
    def Quit(self):
        self.after(500, self.destroy)
        
        
        

if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    except Exception as msg:
        print(f"Locale message: {msg}")        
    
    app = Application()
    # -------------------------------------------------------------------------
    if sys.platform=='win32':
        app.iconbitmap(default=osp.join(os.getcwd(),'imgsDataDB','carddb.ico'))
    else:
        icon = tk.PhotoImage(master=app, file=osp.join(os.getcwd(),'imgsDataDB','carddb.gif'))
        app.wm_iconphoto(True, icon)
    # -------------------------------------------------------------------------
    app.title("CARDDB Handler v1.0 (c)2025 AMOUROUX Bernard - GUI de saisie des cartes de CARDDB (c)2026 AMOUROUX Jan")
    app.mainloop()
        