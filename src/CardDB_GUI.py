# -- encode utf-8 --
"""
CARDDB Handler - Une étude Python POO pour la saisie des données des types de cartes 
'creature', 'equipement' et 'spell' du jeu CARDDB en mode graphique (TKinter).
Copyright (c) 2026 Jan AMOUROUX - étude moteur du jeu pour la création des cartes. 
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

GPL3 License - CARDDB (c) 2026 Jan AMOUROUX 
GPL3 License - CARDDB Handler GUI (c) 2026 Bernard AMOUROUX

This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Bernard AMOUROUX"
__date__ = "$Date: 2026/08/01 07:00 $"
__copyright__ = "Copyright (c) 2026 Bernard AMOUROUX"
__license__ = "GPL 3"

from imaplib import Commands
import locale
import os, sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path as osp
import shutil

from re import sub
from Card import Card
from SpellCard import Spell
from PIL import Image,ImageTk
from TerrainCard import Terrain
from main import writeFile,readFile
from typing import Literal,get_args
from tkinter.filedialog import askopenfilename
from equipmentCard import Equipment
from CreatureCard import Creature
from cardLogics import readRules
from tkinter.font import Font

ITEMSTYPE = Literal["Effets","Eléments","Races","Talents"]
itemstypeList = get_args(ITEMSTYPE)

class My_LabelFrame(tk.LabelFrame):
    """ classe héritant de tkinter.LabelFrame() qui se crée et se place 
        sur la grille en une ligne de commandes. Par défaut, la couleur de fond
        sera 'ivoire', une largeur de bordure de 3, un relief de périmètre 'groove'
        et un ancrage de label s'il y a au centre en haut. 
    """
    def __init__(self,master,col=0,row=0,cspan=1,rspan=1,pad=(0,0,0,0),sticky='nsew', *args, **kwargs):

        tab_options:dict = {'bg':'ivory', 'bd':3, 'relief':'groove', 'labelanchor':'n'}
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)

        super().__init__(master,*args,**kwargs)        

        self.grid(column=col, row=row, columnspan=cspan, rowspan=rspan,
                                  padx=pad[0], pady=pad[1], ipadx=pad[2], ipady=pad[3], sticky=sticky)
        self.columnconfigure(list(range(cspan)), weight=1)
        self.rowconfigure(list(range(rspan)), weight=1)

    def name(self):
        return f"{self.master}."+self._name

        
class Window_StateBar(tk.Frame):
    """ Classe créant une barre d'état configurable qui permet l'affichege d'un message
        d'état pendant une durée déterminée, indéterminée ou immédiate.
        Méthodes de la classe:
            update_vltexte : 
                msg  : message à afficher
                wait : temps d'affichge du message. défaut 10s
            tips: wait à 1 pour que le message s'affiche en permanence sans changer defMessage    
            message :
                getter : extrait le message en cours.
                setter : définit le message par défaut
            tips: pour que le message par défaut soit affiché imméditement, exécuter 'update_vltexte("",0)'                              
    """
    def __init__(self, master, message:str, waitime:int, col=0, row=0, cspan=1, sticky="nsew",
                        defMessage:str=' Info : ', defTime:int=10, txtfont=None, *args, **kwargs):
        """
        Attributs du constructeur:
            master     : Fenètre appelant, objet tkinter.Tk()
            message    : message à afficher apès l'initialisation pendant 10s par défaut ou par 'waitime'
            waitime    : temps définissant la durée d'affichage des message avant le retour du message par défaut
            col, row   : colone et ligne pour le placement dans la grille de la fenètre principale
            rspan, cspan, sticky : paramètres d'extension des lignes et colones dans la grille
            defMessage : message défaut qui s'affiche dès la tempo message terminée.
            defTime    : durée d'affichage des message par défaut 
            txtfont    : police de caractères pour l'affichage des messages
        """
        self.__master = master
        self.__message = message
        self.__waitnbr:int = None
        self.__defaultTime = defTime
        self.__defaultMsg = defMessage
        self.__vl_texte = tk.StringVar()
        self.__wait = waitime

        tab_options:dict = {'bd':1, 'bg':'tan2', 'relief':'groove'}        
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)
        super().__init__(master, *args, **kwargs)
        
        lblfont = ("Courier New",10 ,'bold','italic') if not txtfont else txtfont
        
        self.grid(column=col,row=row,columnspan=cspan,padx=2,pady=2,sticky=sticky)
        
        tk.Label(self,bd=0,bg=self.cget('bg'),anchor="sw",height=1,font=lblfont,textvariable=self.__vl_texte).grid()
        self.update_vltexte(defMessage if message=="" else message, waitime)

    def __raz_vltexte__(self):
        """ methode privée de mise au message par défaut """
        self.__vl_texte.set(self.__defaultMsg)
        self.__waitnbr = None
    
    def update_vltexte(self, msg:str, wait=10):
        """ méthode de chargement d'un nouveau message pour affichage le temps désiré """
        if self.__waitnbr != None:
            self.after_cancel(self.__waitnbr)
        if wait == 0:
            self.__raz_vltexte__()
        elif wait > 1:
            self.__waitnbr = self.after(self.__defaultTime if wait==None else (wait*1000) , self.__raz_vltexte__)
            self.__vl_texte.set(msg)            
        elif wait == 1:    
            self.__vl_texte.set(msg)
        super().update_idletasks()

    @property
    def message(self) -> str:
        return self.__vl_texte.get().rstrip()
    @message.setter
    def message(self, message:str):
        self.__defaultMsg = message


class Win_MessageBox(tk.Toplevel):
    """ Classe fournissant une boite de message pour une l'application principale. Une fois initialisé,
        la fenètre se masque automatiquement et se rend visible lorsqu'on demande à afficher un message.
        Se masque à nouveau après la validation par ok. Se détruit lorsque l'on quitte l'application.
        Methodes de la classe:
            boxtitle : définit le texte de la barre de titre de la fenètre 
            message  : 
                getter: pour extraire le message en cours
                setter: pour monter et afficher la fenètre au premier plan,
                        intercepter tous les évènements, et afficher le message.
                        Une fois le bouton ok validé, rend la gestion des évènements
                        à l'appelant et la fenètre se masque.
            textfont : change la police de caractère pour les messages suivants    
    """
    def __init__(self, master, message:str=None, msgtext=('Consolas 11 bold italic'), *args, **kwargs):
        """ Attributs du constructeur: 
                master : objet tkinter.Tk() ou tkinter.Toplevel()
                message (str): texte qui sera affiché dans la fenètre
                msgtext : police de caractères des messages d'information
        """    
        self.__master = master
        self.__name__ = 'win_messagebox'
        self.__vmessage = tk.StringVar(value=message)
        
        tab_options:dict = {'bd':3, 'bg':'ivory2', 'relief':'ridge', 'pady':5}        
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)
        super().__init__(master, *args, **kwargs)
        
        self.protocol("WM_DELETE_WINDOW", self.Quit)
        self.wm_attributes("-topmost", 1)                     # - Fenetre popup toujours au premier plan
        self.resizable(False, False)
        self.grid_anchor('center')
        
        self.messageBox = tk.Message(self,bg=self.cget('bg'),width=450,aspect=100,justify=tk.CENTER,
                                                        font=msgtext,textvariable=self.__vmessage)
        self.messageBox.grid(column=0,row=0,padx=20,pady=10,sticky="nsew")
        tk.Button(self,width = 8,bg='tan',text='Ok',command=self.Quit).grid(column=0,row=1,sticky="n")
        self.bind('<Return>', self.Quit)
        self.withdraw()
    
    @property
    def message(self)->str:
        """ Retourne le message en cours """
        return self.__vmessage.get()
    
    @message.setter
    def message(self, message):
        """ Met à jour la variable dynamique et affiche un message  """
        self.__vmessage.set(message)
        if not self.winfo_ismapped():
            self.deiconify()
            self.grab_set()
            self.lift()
        self.update()
    
    def textfont(self, msgtext:str):
        """ Configure la police de caractères pour l'affichage du message """
        self.messageBox.configure(font=msgtext)
        
    def boxtitle(self, title:str):
        """ Crée, remplace le titre principal """
        self.title(title)
    
    def Quit(self, event=None):
        """ Quitte par tk.Toplevel.withdraw() et NON destroy()
            Rend à l'appelent l'interception des évènements.
            La fenètre se masque.
        """
        self.boxtitle(" Message ")
        self.grab_release()
        self.withdraw()    
   
    
class List_Popup(tk.Toplevel):
    """ Affichage d'une fenetre popup toujours au premier plan sans boutons système
        Se ferme après avoir choisi un élément dans la liste.
    """
    Popup_Show:bool = True
    
    def __init__(self, master, liste:tk.StringVar, cardtype:str, *args, **kwargs):
        
        if not liste.get(): return

        self.__master = master
        self.__vliste = liste

        tab_options:dict = {'bd':2, 'bg':'orange', 'relief':'flat'}        
        for key in list(tab_options.keys()):
            if kwargs.get(key, None) == None: kwargs[key] = tab_options.get(key, None)
        super().__init__(master, name=f"!list_popup{cardtype}", **kwargs)
        
        lst_font = Font(family='Consolas',size=12,weight='normal',slant='italic')    
        frm_font = Font(family="Courier New",size=10,weight="normal",slant="italic")
        
        self.wm_attributes("-topmost", 1)                     # - Fenetre popup toujours au premier plan
        self.bind_class(self,'<Button1-Motion>',self.motion)  # - Bouton droit pour déplacer la fenètre popup
        #self.bind_class(self,"<Button-3>", self.Quit)         # - pour quitter la popupList par 'Clic Gauche'
        self.overrideredirect(1)                              # - Aucun bouton systeme sur la fenetre   
        
        # --------- frame avec widget label et widget liste des items --------- 
        frame = My_LabelFrame(self, bd=0, bg='wheat', relief='flat',text=f" Liste des {cardtype} ",font=frm_font)
        self.lst = tk.Listbox(frame,bg='ivory',bd=0,activestyle='none',relief="flat",listvariable=self.__vliste)
        self.lst.configure(font=lst_font,selectbackground='ivory',selectforeground='black')
        self.lst.grid(column=0,row=0,sticky="nsew")
        self.lst.update()
        
        # ------------ récupération coordonnées fenètre principale ------------
        self.__master.update_idletasks()
        main_x = self.__master.winfo_rootx()
        main_y = self.__master.winfo_rooty()
        main_w = self.__master.winfo_width()
        # --------------- récupération coordonnées fenètre popup --------------
        popup_w = self.winfo_width()
        popup_h = self.winfo_height()

        offset = self.get_offset()
        #print(f"offset: {offset}")
        
        x = main_x + main_w + (offset//15)
        y = main_y + offset
        self.geometry(f"{popup_w}x{popup_h}+{x}+{y}")
        self.update(); pos = self.geometry()
        self.lst_pos = f"{pos[:pos.find('+')]}"
        # ------- positionnement de la fenetre fonction position souris -------   
        #pos = self.geometry()                                 # - position fenetre popup 
        #mousexy = master.winfo_pointerxy()                    # - Récupère la position de la souris  
        #self.lst_pos = f"{pos[:pos.find('+')]}"
        #self.geometry(f"{self.lst_pos}+{mousexy[0]+200}+{mousexy[1]-100}")
        self.update_idletasks()

    def update_list(self, liste:list|set):
        if len(liste) > 0 and isinstance(liste, set):
            liste.discard("None")
            liste = list(liste)
        self.__vliste.set(liste)
        
    def get_offset(self) -> int:
        return (len(list(filter(lambda name: "!list_popup" in name,self.__master.children.keys())))-1)*60
        
    def motion(self, event):
        mousexy = self.__master.winfo_pointerxy()
        self.geometry(f"{self.lst_pos}+{mousexy[0]}+{mousexy[1]}")
        
    def Quit(self, event:tk.Event=None):
        """ Sortie de la boucle principale et non fermeture de la fenetre """
        self.destroy()           # Exit mainloop()



class PopupMenu(tk.Menu):
    """ Classe Menu popup paramétrable.
        Les parametres du contructeur sont:
            'master': widget appelant doit etre un tk.Toplevel()
            'title' : titre du popup menu mis en surbrillance continue.
            Les 2 paramètres suivants indiquent les actions du menu.
            'commandsList': tuple de la forme (label_cmd:str, accel_cmd:str, commande:list[callable])
            'nosel' : list[int] liste des indices des rubrique dont l'état sera 'disabled' 
        Les méthodes de la classe sont:
            show_Menu_popup()   : affiche le menu popup à l'endroit du clic droit souris.
            nomenupopup(NoSel)  : prend en paramètre une liste contenant les numéros des rubriques à dévalider.
        La propriété 'NoSel' getter/setter sert de paramètre à la méthode 'nomenupopup()'.
    """
    def __init__(self, master:tk.Tk, title:str, commandsList:tuple=None, nosel:list=None):
        
        self.__master = master
        self.__commandList = commandsList
        self.__title = title.split(',')
        self.__NoSel = nosel
        
        super().__init__(master,tearoff=0,font=('Arial 12 bold italic'),postcommand=lambda :self.nomenupopup(self.__NoSel))
            
    def show_Menu_Popup(self, event:tk.Event):
        # ---------------------------------------------------------------------
        self.delete(0, 'end')   # -- reset de la liste des commandes ajoutées -
        if len(self.__title) == 1: self.__title = (self.__title, " ")
        self.add_command(label=self.__title[0],accelerator=self.__title[1],background='orange',activebackground='orange')
        self.configure(background="ivory", activebackground='tan',borderwidth=2,relief="solid")
        self.add_separator()
        self.add_Popup_Commands(commands=self.__commandList)
        self.nomenupopup(self.NoSel)
        # ---------------------------------------------------------------------
        try:
            self.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"Erreur interne : {e}")
            self.grab_release()
    
    @property
    def NoSel(self) -> list:
        return self.__NoSel
    @NoSel.setter
    def NoSel(self, nosel:list):
        self.__NoSel = nosel
             
    def nomenupopup(self, nosel:list):                
        [self.entryconfigure(i, state = 'disabled') for i in nosel]

    def add_Popup_Commands(self, commands:tuple):
        for command in commands:
            if command[0] == "separator":
                self.add_separator()
            else:
                self.add_command(label=command[0],accelerator=command[1],command=command[2])   
        

class Application(tk.Tk):
    
    def __init__(self):
        
        super().__init__(className = "Tk", useTk = True)

        self.ttlfont = Font(self, family='Courier',size=14,weight='bold',slant='italic')
        self.lblfont = Font(self, family='Consolas',size=10,weight='bold',slant='italic')
        self.itemfont= Font(self, family='Courier New',size=12,weight='bold',slant='italic')
        self.cmbfont = Font(self, family='Consolas',size=16,weight='normal',slant='italic')
        self.chkfont = Font(self, family='Consolas',size=8,weight='bold',slant='italic')
        self.frmfont = Font(self, family="Times", size=12, weight="bold", slant="roman")
        # ---------------------------------------------------------------------
        self.MessageBox = Win_MessageBox(self, msgtext=('Courier New', 14, 'normal', 'italic'))  
        self.state_bar = Window_StateBar(self,"",0,0,10,cspan=18,bg='tan',pady=3,txtfont=self.lblfont)                                         
        self.state_bar.message = " Info : 'Clic-Droit' ou 'Ctrl-M' pour le menu contextuel de CardDB-GUI v2.0"
        self.backup_bar = Window_StateBar(self,"",0,18,10,cspan=4,bg='wheat',pady=3,txtfont=self.lblfont)
        self.backup_bar.message = " Info : Aucune liste déroulante sauvegardée "
        # ---------------------------------------------------------------------
        self.button_add = tk.PhotoImage(file=osp.join("./","imgsDataDB","add-file-32.png"))
        self.button_suppr = tk.PhotoImage(file=osp.join("./","imgsDataDB","delete-file-32.png"))
        self.button_liste = tk.PhotoImage(file=osp.join("./","imgsDataDB","list-32.png"))
        # ---------------------------------------------------------------------
        self.protocol('WM_DELETE_WINDOW',self.Quit)
        # --- Création virtual-Event Ajout/Suppression items des Combobox -----
        self.event_add("<<ComboboxAddItem>>","<Return>","<KP_Enter>","<FocusOut>")
        self.event_add("<<ComboboxDelItem>>","<Delete>","<KP_Delete>","<BackSpace>")
        # ------------- Création virtual-Event menu contextuel ----------------
        self.event_add("<<PopupMenu>>","<Control-M>","<Control-m>","<Button-3>")
        # ----------------------- EDT main poup menu --------------------------
        commandsList = [(" Backup des Listes en quittant"," On/Off ",self.__toggle_backupList),
                        ("separator","",None),
                        (" Mode plein écran on/off","F11",self.__toggle_fullscreen),
                        ("separator","",None),
                        (" A propos de OGG","",self.fenetre_a_propos),
                        (" Aide de OGG","F1",None),
                        ("separator","",None),
                        (" Quitter OGG "," Alt-F4 ",self.Quit)]
        self.cardDBMenu = PopupMenu(self, "        CardDB-GUI v2.0, PopupMenu", commandsList, nosel=[7])
        # ---------------------------------------------------------------------
        self.bind('<F1>', self.fenetre_a_propos)
        self.bind("<F11>",self.__toggle_fullscreen)
        self.bind("<Escape>", self.__exit_fullscreen)
        self.bind_class(self, "<<PopupMenu>>", self.cardDBMenu.show_Menu_Popup)
        self.columnconfigure(list(range(20)), minsize=40, weight=1)
        self.columnconfigure(index=[20,21], minsize=90, weight=1)
        self.rowconfigure(list(range(11)), minsize=32, weight=0)
        #self.rowconfigure(index=[7,8], minsize=32, weight=1)
        self.minsize(width=1024, height=380)
        self.grid_anchor('w')
        
        self.init_variables()
        self.cree_widgets()
        self.update()
    
    def init_variables(self):
        """ Définition de toutes les variables de type tkinter.StringVar() ou tkinter.Inrvar()
            utilisées par l'application.
        """
        self.cardtypelist:list = ["creature", "equipement", "spell", "terrain"]
        self.vcardimageFname = tk.StringVar(value="placeholder.png")
        self.vcardDBFname = tk.StringVar(value="default.json")
        self.vcardtype = tk.StringVar(value=self.cardtypelist[0])
        self.itemtypelist:list = ["arme","armure"]
        self.vitemtype = tk.StringVar(value=self.itemtypelist[0])
        self.typesortlist:list = readRules('sort')
        self.vtypesort = tk.StringVar(value=self.typesortlist[0])
        self.curencytypelist:list = readRules('monnaie')
        self.vcurencytype = tk.StringVar(value=self.curencytypelist[-1])
        self.talentstypelist:list = readRules('talents')
        self.vtalentstype = tk.StringVar(value=self.talentstypelist[-1])
        self.multitalentlist = set()
        self.elementstypelist = readRules('elements')
        self.velementstype = tk.StringVar(value=self.elementstypelist[-1])
        self.multielementlist = set()
        self.armeslist = readRules('armes')
        self.varmes = tk.StringVar(value=self.armeslist[-1])
        self.varmesequip = tk.StringVar(value=self.armeslist[1])
        self.monnaielist = readRules('monnaie')
        self.vmonnaie = tk.StringVar(value=self.monnaielist[0])
        self.raceslist = readRules('races')
        self.vraces = tk.StringVar(value=self.raceslist[3])
        self.racesequiplist = readRules('races') + ["None",]
        self.vracesequip = tk.StringVar(value=self.racesequiplist[-1])
        self.multiracequiplist = set()
        self.typeffetlist = readRules('effets') 
        self.veffects = tk.StringVar(value=self.typeffetlist[-1])
        self.multieffetlist = set()
        # ---- variables de controle des tk.Checkbutton() 'backup listes' -----
        self.vbackupEffets = tk.IntVar(value=0);    self.vbackupTalents = tk.IntVar(value=0)
        self.vbackupElements =tk.IntVar(value=0);   self.vbackupRaces = tk.IntVar(value=0)
        self.cbox_textvariable_dico:dict = { "Effets":self.vbackupEffets,    "Eléments"  :self.vbackupElements,
                                             "Races":self.vbackupRaces,      "Talents"   :self.vbackupTalents   }
        # ---------------------------------------------------------------------
        self.multiSetlist = [self.multielementlist,self.multiracequiplist,self.multieffetlist,self.multitalentlist] 
        self.items_dico:dict = {"Eléments": self.multielementlist, "Races":   self.multiracequiplist,
                                "Effets":   self.multieffetlist,   "Talents": self.multitalentlist  }
        self.typeItems_Dico:dict = {z[0]:(z[1],z[2]) for z in zip(list(self.items_dico.keys()),
                      [self.velementstype,self.vracesequip,self.veffects,self.vtalentstype],self.multiSetlist)}
        self.__saveItemsList_onQuit: bool = False
        self.popup_dico:dict = {}
        # ---------------------------------------------------------------------
        self.vname = tk.StringVar()
        self.vmastertitle = tk.StringVar(value=" Type de carte à créer :")
        self.vlabelname = tk.StringVar(value=" Nom de la créature à créer :")
        self.vcost = tk.IntVar(value=1)
        self.vhp = tk.IntVar(value=0)
        self.vheal = tk.IntVar(value=0)
        self.typecritlist:list = [0,2,6,8,20]
        self.vtypecrit = tk.IntVar(value=self.typecritlist[0])
        self.typetargetlist:list = ["mono","zone","groupe","None"]
        self.vtypetarget = tk.StringVar(value=self.typetargetlist[0]) 
        self.vatk = tk.IntVar(value=0)
        self.vdef = tk.IntVar(value=0)
    
    def cree_widgets(self):
        """ Création de tous les widgets de la fenètre principale
            Configuration et affichage/masquage des widgets en dynamique (gestion des évènements)
        """
        globalframe = My_LabelFrame(self,cspan=20,rspan=9,pad=(2,2,2,2),name="!globalFrame",sticky="nsew")
        # --- Création du tk.Canvas() pour affichage de l'image de la carte ---
        imageframe = My_LabelFrame(self,col=20,cspan=2,rspan=9,bg='wheat',pad=(2,2,2,2),sticky="new")
        self.cardDBcanvas = tk.Canvas(imageframe, bd=3, relief='ridge', bg='ivory2', 
                                                            width=200,height=320,name="!cardDBcanvas")
        self.cardImage = self.preload_cardDB_Image("placeholder.png")
        self.cardDB_image = self.cardDBcanvas.create_image(+7,+5, image=self.cardImage, 
                                                        state="normal",anchor="nw",tags='img_default')
        self.cardDBcanvas.grid(column=0,row=0,columnspan=2,rowspan=9,sticky='new')
        # ----- Création visuel pour affichage des elements,races,effets ------
        titleframe = My_LabelFrame(globalframe,col=2,row=0,cspan=16,bg="#FBE6C8",
                                                        pad=(2,2,0,0),name="!titleFrame",sticky="ew")
        tk.Label(titleframe,textvariable=self.vmastertitle,bg=titleframe.cget('bg'),
                                      font=self.ttlfont).grid(column=0,row=0,columnspan=8,sticky="new")
        self.comboxCardType = ttk.Combobox(titleframe,background=titleframe.cget('bg'),
                                    font=self.cmbfont,postcommand=None,values=self.cardtypelist,
                                             state="readonly",name="!comboxCardType",textvariable=self.vcardtype)
        self.comboxCardType.grid(column=8,row=0,columnspan=8,sticky="new")
        self.comboxCardType.bind("<<ComboboxSelected>>",self.specificFrame)
        # ---------------------------------------------------------------------
        # ------- frame des attributs communs à toutes les carte CardDB -------
        # ---------------------------------------------------------------------
        self.frameCardDB = My_LabelFrame(globalframe,col=0,row=1,cspan=20,rspan=2,bg=globalframe.cget('bg'),
                                          name="!frameCardDB",pad=(2,0,0,0),bd=2,relief="groove",sticky="new")
        tk.Label(self.frameCardDB,bg=self.frameCardDB.cget('bg'),textvariable=self.vlabelname,
                            anchor="w",font=self.itemfont).grid(row=0,column=0,columnspan=4,pady=4,sticky="nw")
        tk.Entry(self.frameCardDB,bg='ivory',textvariable=self.vname,
                            font=self.itemfont).grid(column=4,columnspan=3,row=0,pady=4,ipady=1,sticky="nw")
        tk.Label(self.frameCardDB,bg=self.frameCardDB.cget('bg'),text="  Type de créature :",name="!labelTypeCreature",
                            anchor="w",font=self.itemfont).grid(row=0,column=9,columnspan=3,pady=4,sticky="nw")
        self.comboxRaceType = ttk.Combobox(self.frameCardDB,background=self.frameCardDB.cget('bg'),
                                      font=self.itemfont,postcommand=None,values=self.raceslist,
                                          state="readonly",name="!typeRaceCombobox",textvariable=self.vraces)
        self.comboxRaceType.grid(column=12,row=0,columnspan=8,padx=2,pady=4,sticky="new")
        tk.Label(self.frameCardDB,text=" Coût de la carte :",bg=self.frameCardDB.cget('bg'),
                        name="!labelCost",font=self.itemfont).grid(row=1,column=0,columnspan=2,pady=4,sticky="nw")
        tk.Entry(self.frameCardDB,bg='ivory',textvariable=self.vcost,width=3,
                        name="!entryCost",font=self.itemfont).grid(column=2,row=1,columnspan=1,pady=4,sticky="nw")
        self.curencyCombobox = ttk.Combobox(self.frameCardDB,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=self.curencytypelist,
                                                state="readonly",name="!comboboxCost",textvariable=self.vcurencytype)
        self.curencyCombobox.grid(column=3,row=1,columnspan=4,padx=5,pady=4,sticky="new")
        tk.Label(self.frameCardDB,text=" Image carte :",bg=self.frameCardDB.cget('bg'),
                               font=self.itemfont).grid(row=1,column=9,columnspan=2,padx=5,pady=4,sticky="nw")
        tk.Entry(self.frameCardDB,bg='ivory',font=self.itemfont,state="readonly",width=20,
                    textvariable=self.vcardimageFname).grid(row=1,column=11,columnspan=4,pady=4,sticky="nw")
        tk.Button(self.frameCardDB,text=" Choisir Image ",command=self.select_imageFile,
                            font=self.lblfont).grid(row=1,column=16,columnspan=2,pady=3,sticky="new")
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        texte = " Données des Armes, Talents et Eléments "
        frametalents = My_LabelFrame(globalframe,col=10,row=3,cspan=10,rspan=4,bg=globalframe.cget('bg'),
                                text=texte,font=self.lblfont,pad=(0,0,0,4),bd=2,relief="ridge",sticky="new") 
        # ---------------------------------------------------------------------
        tk.Label(frametalents,text=" Talent         : ",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=0,column=0,columnspan=2,pady=4,sticky="nw")
        self.talentsCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),
                                 font=self.itemfont,state="readonly",name="!talentsCombobox",width=10,
                                   postcommand=None,values=self.talentstypelist,textvariable=self.vtalentstype)
        self.talentsCombobox.grid(column=2,row=0,columnspan=8,padx=2,pady=4,sticky="new")
        self.talentsCombobox.bind("<<ComboboxAddItem>>",self.__update_comboboxValues)
        self.talentsCombobox.bind("<<ComboboxDelItem>>",self.__delete_comboboxValues)
        # ---------------------------------------------------------------------
        tk.Label(frametalents,text=" Arme équipable : ",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=1,column=0,columnspan=2,pady=0,sticky="nw")
        self.armesCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),
                                            font=self.itemfont,postcommand=None,values=list(self.armeslist),
                                                state="readonly",name="!armesCombobox",textvariable=self.varmes)
        self.armesCombobox.grid(column=2,row=1,columnspan=8,padx=2,pady=0,sticky="new")
        # ---------------------------------------------------------------------
        tk.Label(frametalents,text=" Eléments :",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=2,column=0,columnspan=3,pady=4,rowspan=2,sticky="w")
        self.elementsCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),width=14,
                                  postcommand=None,values=list(self.elementstypelist),font=self.itemfont,
                                    state="readonly",name="!elementsCombobox",textvariable=self.velementstype)
        self.elementsCombobox.grid(column=1,row=2,columnspan=5,padx=2,pady=4,rowspan=2,sticky="e")
        self.elementsCombobox.bind("<<ComboboxAddItem>>",self.__update_comboboxValues)
        self.elementsCombobox.bind("<<ComboboxDelItem>>",self.__delete_comboboxValues)
        tk.Button(frametalents,compound="center",image=self.button_add,height=32,width=32,
                                 command=lambda: self.__add_items__("Eléments")).grid(column=6,
                                                         row=2,padx=0,pady=3,columnspan=2,rowspan=2,sticky="w")
        tk.Button(frametalents,compound="center",image=self.button_suppr,height=32,width=32,
                                    command=lambda :self.__del_items__("Eléments")).grid(column=7,
                                                         row=2,padx=0,pady=3,columnspan=2,rowspan=2,sticky="e")
        tk.Button(frametalents,compound="center",image=self.button_liste,height=32,width=32,
                                    command=lambda :self.__list_items__("Eléments",False)).grid(column=9,
                                                         row=2,padx=2,pady=3,columnspan=2,rowspan=2,sticky="e")
        # ---------------------------------------------------------------------
        self.frameBackuplistes = My_LabelFrame(frametalents,bd=1,col=0,row=4,bg='wheat',
                                                                   cspan=10,relief="sunken",pad=(0,0,3,2))                               
        tk.Label(self.frameBackuplistes,text=" Modifier les :",bg=self.frameBackuplistes.cget('bg'),
                                font=('Consolas 8 bold italic')).grid(column=0,row=0,sticky="nsew")
        tk.Checkbutton(self.frameBackuplistes,variable=self.vbackupEffets,text="Effets",
                         font=self.chkfont,command=lambda: self.__update_ComboboxState("Effets"),
                               bg=self.frameBackuplistes.cget('bg')).grid(column=1,row=0,sticky="nsew")
        tk.Checkbutton(self.frameBackuplistes,variable=self.vbackupElements,text="Eléments",
                        command=lambda: self.__update_ComboboxState("Eléments"),font=self.chkfont,
                               bg=self.frameBackuplistes.cget('bg')).grid(column=3,row=0,sticky="nsew")
        tk.Checkbutton(self.frameBackuplistes,variable=self.vbackupTalents,text="Talents",font=self.chkfont,
                command=lambda: self.__update_ComboboxState("Talents"),name="!chkbtnBackupTalents",
                      bg=self.frameBackuplistes.cget('bg')).grid(column=5,row=0,sticky="nsew")
        tk.Checkbutton(self.frameBackuplistes,variable=self.vbackupRaces,text="Races",font=self.chkfont,
                command=lambda: self.__update_ComboboxState("Races"),name="!chkbtnBackupRace",
                      bg=self.frameBackuplistes.cget('bg'),state="disabled").grid(column=7,row=0,sticky="nsew")
        # ---------------------------------------------------------------------
        texte = " Données statistiques de combat "
        frameproperty = My_LabelFrame(globalframe,col=0,row=3,cspan=10,rspan=4,bd=2,bg=globalframe.cget('bg'),
                                               font=self.lblfont,text=texte,pad=(0,0,0,3),relief="ridge",sticky="new")  
        tk.Label(frameproperty,text=" Points de vie    : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=0,column=0,columnspan=4,pady=0,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vhp,width=3,
                                  font=self.itemfont).grid(column=4,row=0,columnspan=1,pady=0,sticky="nw")
        tk.Label(frameproperty,text=f" {'Soin':<18}: ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=0,column=5,columnspan=3,pady=0,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vheal,width=3,
                                  font=self.itemfont).grid(column=8,row=0,columnspan=2,pady=0,sticky="nw")
        tk.Label(frameproperty,text=" Points d'attaque : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=1,column=0,columnspan=4,pady=3,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vatk,width=3,
                                  font=self.itemfont).grid(column=4,row=1,columnspan=1,pady=3,sticky="nw")
        tk.Label(frameproperty,text=" Points de défense :",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=1,column=5,columnspan=3,pady=3,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vdef,width=3,
                                  font=self.itemfont).grid(column=8,row=1,columnspan=2,pady=3,sticky="nw")
        tk.Label(frameproperty,text=" Valeur critique  : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=2,column=0,columnspan=4,sticky="nw")
        ttk.Spinbox(frameproperty,background='ivory',command=None,font=self.itemfont,
                                      values=self.typecritlist,width=3,textvariable=self.vtypecrit,
                                            state="readonly",wrap=True).grid(column=4,row=2,pady=0,sticky="nw")
        # ---------------------------------------------------------------------
        tk.Label(frameproperty,text=" Ciblage     : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=2,column=5,columnspan=2,pady=0,sticky="nw")
        self.targetCombobox = ttk.Combobox(frameproperty,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=list(self.typetargetlist),
                                                state="readonly",name="!targetCombobox",textvariable=self.vtypetarget)
        self.targetCombobox.grid(column=7,row=2,columnspan=3,padx=2,pady=3,sticky="nw")
        # ---------------------------------------------------------------------
        tk.Label(frameproperty,text=f" {'Effets':<17}: ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=3,column=0,columnspan=4,pady=3,sticky="w")
        self.effetsCombobox = ttk.Combobox(frameproperty,background=globalframe.cget('bg'),width=10,
                                       postcommand=None,values=list(self.typeffetlist),font=self.itemfont,
                                            state="readonly",name="!effetsCombobox",textvariable=self.veffects)
        self.effetsCombobox.bind("<<ComboboxAddItem>>",self.__update_comboboxValues)
        self.effetsCombobox.bind("<<ComboboxDelItem>>",self.__delete_comboboxValues)
        self.effetsCombobox.grid(column=4,row=3,columnspan=3,pady=3,sticky="ew")
        tk.Button(frameproperty,compound="center",image=self.button_add,height=32,width=32,
                                      command=lambda :self.__add_items__("Effets")).grid(column=7,
                                                        row=3,padx=3,pady=3,columnspan=2,sticky="nsw")
        tk.Button(frameproperty,compound="center",image=self.button_suppr,height=32,width=32,
                                       command=lambda :self.__del_items__("Effets")).grid(column=7,
                                                            row=3,padx=0,pady=3,columnspan=3,sticky="ns")
        tk.Button(frameproperty,compound="center",image=self.button_liste,height=32,width=32,
                                    command=lambda :self.__list_items__("Effets",False)).grid(column=8,
                                                               row=3,padx=3,pady=3,columnspan=2,sticky="nse")
        # ---------------------------------------------------------------------
        # ----------- frame des attributs spécifiques à Equipement ------------
        # ---------------------------------------------------------------------
        self.equipementFrame = My_LabelFrame(globalframe,col=0,row=7,cspan=20,rspan=2,
                                                                  bg="#E9FAD8",name="!equipementFrame",sticky="sew")
        # ---------------------------------------------------------------------
        tk.Label(self.equipementFrame,anchor="w",bg=self.equipementFrame.cget('bg'),text=" Mode de défense :",
                                                    font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="w")
        self.equipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                                font=self.itemfont,postcommand = None,values=self.itemtypelist,
                                                    state="readonly",name="!equipCombobox",textvariable=self.vitemtype)
        self.equipCombobox.bind("<<ComboboxSelected>>",self.__valide_armequipement)
        self.equipCombobox.grid(column=2,row=0,columnspan=4,pady=2,sticky="w")
        # ---------------------------------------------------------------------
        tk.Label(self.equipementFrame,text=" Type d'arme :",bg=self.equipementFrame.cget('bg'),
                               font=self.itemfont).grid(row=1,column=0,columnspan=2,sticky="w")
        self.armesEquipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                    font=self.itemfont,postcommand=None,values=list(self.armeslist),
                                                state="readonly",name="!armequipCombobox",textvariable=self.varmesequip)
        self.armesEquipCombobox.grid(column=2,row=1,columnspan=4,pady=2,sticky="w")
        self.armesEquipCombobox.set(self.armeslist[2])
        # ---------------------------------------------------------------------
        tk.Label(self.equipementFrame,text=" Races équipées :",bg=self.equipementFrame.cget('bg'),
                               font=self.itemfont).grid(row=0,column=7,columnspan=3,rowspan=2,sticky="w")
        self.racesEquipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                               postcommand=None,values=list(self.racesequiplist),font=self.itemfont,
                                                   state="readonly",name="!racesCombobox",textvariable=self.vracesequip)
        self.racesEquipCombobox.grid(column=10,row=0,columnspan=7,rowspan=2,pady=2,sticky="w")
        self.racesEquipCombobox.bind("<<ComboboxAddItem>>",self.__update_comboboxValues)
        self.racesEquipCombobox.bind("<<ComboboxDelItem>>",self.__delete_comboboxValues)
        tk.Button(self.equipementFrame,compound="center",image=self.button_add,height=32,width=32,
                                           command=lambda: self.__add_items__("Races")).grid(column=17,
                                                                    row=0,padx=3,pady=3,rowspan=2,sticky="w")
        tk.Button(self.equipementFrame,compound="center",image=self.button_suppr,height=32,width=32,
                                             command=lambda :self.__del_items__("Races")).grid(column=18,
                                                                    row=0,padx=0,pady=3,rowspan=2,sticky="w")
        tk.Button(self.equipementFrame,compound="center",image=self.button_liste,height=32,width=32,
                                       command=lambda: self.__list_items__("Races", False)).grid(column=19,
                                                                    row=0,padx=3,pady=3,rowspan=2,sticky="w")
        # ---------------------------------------------------------------------
        # -------------- frame des attributs spécifiques à Sort ---------------
        # ---------------------------------------------------------------------
        self.spellFrame = My_LabelFrame(globalframe,col=0,row=7,cspan=20,rspan=2,bg="#D8E6FA",name="!spellFrame",sticky="sew")
        tk.Label(self.spellFrame,anchor="center",bg=self.spellFrame.cget('bg'),text=f"{' Type de sort :':>20}",
                                              font=self.itemfont).grid(row=0,column=0,columnspan=2,pady=14,sticky="w")
        self.spellCombobox = ttk.Combobox(self.spellFrame,background=self.spellFrame.cget('bg'),
                                        font=self.itemfont,postcommand=None,values=self.typesortlist,
                                             state="readonly",name="!spellCombobox",textvariable=self.vtypesort)
        self.spellCombobox.grid(column=2,row=0,columnspan=4,pady=14,sticky="w")
        """
        # ------------ frame des attributs spécifiques au terrain -------------
        self.terrainFrame = My_LabelFrame(globalframe,col=0,row=6,cspan=20,rspan=2,bg="#F3D6B6",name="!terrainFrame",sticky="sew")
        tk.Label(self.terrainFrame,anchor="center",bg=self.terrainFrame.cget('bg'),text=f"{' Type d\'effet :':>20}",
                                              font=self.itemfont).grid(row=0,column=0,columnspan=2,pady=14,sticky="w")
        self.terrainCombobox = ttk.Combobox(self.terrainFrame,background=self.terrainFrame.cget('bg'),
                                            font=self.itemfont,postcommand=None,values=self.typeffetlist,
                                              state="readonly",name="!terrainCombobox",textvariable=self.veffects)
        self.terrainCombobox.grid(column=2,row=0,columnspan=4,pady=14,sticky="w")
        tk.Button(self.terrainFrame,text="Ajouter/Visualiser la liste des effets",font=self.lblfont,
                                command=self.__add_effect).grid(column=6,row=0,columnspan=14,padx=3,pady=14,sticky="ew")
        """
        # ----------------- frame boutons save/default/cancel -----------------
        buttonsFrame = My_LabelFrame(self,col=0,row=9,cspan=22,pad=(2,0,0,3))
        tk.Button(buttonsFrame,text=" RàZ Défaut ",bg="#FDEED0",command=self.__raz_default,
                                            font=self.frmfont).grid(column=2,row=0,columnspan=3,sticky="ew")
        
        tk.Button(buttonsFrame,text=" Charger/Modifier ",bg="#D0E9FD",command=self.load_CARDDB_file,
                                            font=self.frmfont).grid(column=8,row=0,columnspan=2,sticky="ew")        
        
        tk.Button(buttonsFrame,bg="#C9FFD3",font=self.frmfont,command=self.__save_CARDDB_card,
                                text=" Enregistrer la carte ").grid(column=13,row=0,columnspan=2,sticky="ew")
        tk.Button(buttonsFrame,text=" Annuler/Quitter ",command=self.Quit,bg="#FCC6C6",
                                           font=self.frmfont).grid(column=18,row=0,columnspan=2,sticky="ew")
        # ---------------------------------------------------------------------
        self.framelist = set({self.equipementFrame,self.spellFrame}) #,self.terrainFrame})
        self.state_bar.update_vltexte("",0); self.backup_bar.update_vltexte("",0)
        self.comboxCardType.event_generate("<<ComboboxSelected>>")
        # ---------------------------------------------------------------------

    def select_imageFile(self) -> str:
        title = "Choix du fichier Image"
        files = os.listdir(Card.ImageOutPath)
        imgtypes = [("Images CardDB", "*.jpg;*.gif;*.png;*.bmp;*.tiff"),("Tous les fichiers", "*"),]
        dummyFile = askopenfilename(title=title,initialfile=files[0],initialdir=Card.ImageOutPath,
                                            filetypes=imgtypes,parent=self,typevariable=self.vcardimageFname)
        if dummyFile:
            self.state_bar.update_vltexte(" Info : Nom de fichier image modifié",3)
            # --- chargement et affichage de la nouvelle image de la carte ----
            path, ext = osp.splitext(dummyFile)
            filename = osp.join(Card.ImageOutPath,
                         f"{self.vcardtype.get()}_{self.vname.get().replace(' ','_')}{ext}")
            # -- Copie du fichier image dans le dossier des Images de CardDB --    
            if not osp.isfile(filename): shutil.copyfile(dummyFile, filename)                
            # -- chargement de la nouvelle image/nouveau nom dans le canevas --
            self.newImage = self.preload_cardDB_Image(osp.basename(filename))
            self.cardDBcanvas.itemconfigure(self.cardDB_image, image=self.newImage)
            # ---------- mise à jour de la variable ...cardimage... -----------
            self.vcardimageFname.set(osp.basename(filename))
        else:
            self.state_bar.update_vltexte(" Info : Aucune modification effectuée !",3)
                
    def preload_cardDB_Image(self, fname:str) -> Image.Image:
        # ---------- fichier images à charger, défaut si nécessaire -----------
        filename = osp.join(os.getcwd(),Card.ImageOutPath,fname)
        defaultfilename = osp.join(os.getcwd(),Card.ImageOutPath,"placeholder.png")
        # ---------------------------------------------------------------------
        image = Image.open(fp=filename if osp.isfile(filename) else defaultfilename, mode='r')
        return ImageTk.PhotoImage(image.resize((200,320), Image.Resampling.LANCZOS), master=self)
        
    def __valide_armequipement(self, event:tk.Event=None):
        combo_dico:dict = {"armure":"disabled"}
        w = event.widget if event else self.equipCombobox
        arme, armequip = w.get(), self.armesEquipCombobox.get()
        self.armesEquipCombobox.configure(state= combo_dico.get(arme, "readonly"))
        self.armesEquipCombobox.set('None' if arme == "armure" else \
                        self.varmesequip.get() if armequip != 'None ' else 'None')
                
    def __show_popup_items(self, event:tk.Event=None, item:ITEMSTYPE=""):
        if self.items_dico.get(item, None) != None:
            return List_Popup(self, tk.StringVar(value=sorted(list(self.items_dico[item]))), item)
        else:
            self.state_bar.update_vltexte(f" Info : modèle de carte CardDB '{item}' non reconnu.")
            
    def __raz_default(self):
        # ------------------ affichage de l'image par defaut ------------------
        self.newImage = self.preload_cardDB_Image("placeholder.png")
        self.cardDBcanvas.itemconfigure(self.cardDB_image, image = self.newImage)
        # --------- suppression complete des fenetres popup ouvertes ----------
        [self.nametowidget(popup).destroy() for popup in list(filter(lambda name:"!list_popup" in name, self.children.keys()))]
        # --------------- RàZ des champs de saisies des widgets ---------------
        self.vhp.set(0); self.vatk.set(0); self.vdef.set(0); self.vheal.set(0); self.vname.set(""); self.vtypecrit.set(0)
        self.velementstype.set('None'); self.vtalentstype.set('None'); self.varmes.set('None'); self.vcost.set(1)
        self.vtypetarget.set('mono') if self.vcardtype.get()=="creature" else self.vtypetarget.set('None')
        self.vracesequip.set('None'); self.veffects.set('None'); self.vcardimageFname.set("")
        # ---------- remise en place du titre Création/Modification -----------
        self.vmastertitle.initialize(" Type de carte à créer :")
        # -------- effacement des listes des effets, elements et races --------
        self.__clear_multisetlist__()
    
    def __clear_multisetlist__(self):
        """ RAZ des listes de self.multiSetlist """
        [setlist.clear() for setlist in self.multiSetlist]

    def get_items(self, item:ITEMSTYPE):
        """ méthode qui renvoi les set() des Effets, Eléments et Races en type(list) 
            paramètre:
                item: choix du set() à renvoyer de type ITEMSTYPE = Effets, Eléments, Races
            renvoi le set() correspondant transtypé en 'list'
        """
        return list(self.items_dico[item])

    def __list_items__(self, item:ITEMSTYPE, update:bool=False):
        """ méthode qui affiche ou cache les fenètres popup qui affichent la
            liste des effets, éléments et races.
            parametres:
                item    : choix de la fenètre à afficher/cacher type(ITEMSTYPE)
                update  : bouléen qui informe la class List_Popup() d'une mise à jour
                          des données de la fenètre popup ou d'une création de celle-ci.
        """
        try:
            popup = self.nametowidget(f"!list_popup{item}")
            popup.update_list(self.get_items(item=item)) if update else popup.Quit()    
        except KeyError:
            if not self.items_dico[item]: self.items_dico[item].add(' ... ')    
            self.popup_dico[item] = self.__show_popup_items(item=item)
        
    def __add_items__(self, item:ITEMSTYPE=None):
        """ Ajoute un Effet, Elément, Race au set() des items correspondants 
            paramètre:
                item :  choix de type ITEMSTYPE à ajouter au set(). N'est ajouté que si 
                        non présent. 
        """
        elide:dict = {"Effets":" l'effet ","Eléments":" l'élément ","Races":" la race "}
        getitem = self.typeItems_Dico[item][0].get()
        self.typeItems_Dico[item][1].add(getitem)
        [self.typeItems_Dico[item][1].discard(i) for i in (""," ... ","None") if len(self.typeItems_Dico[item][1]) > 1]
        if not (self.typeItems_Dico[item][1] & set({""," ... ","None"})):
            self.state_bar.update_vltexte(f" Info : Ajout de{elide[item]}'{getitem}' à la liste des effets effectué.", 3)        
        self.__list_items__(item=item, update=True)
            
    def __del_items__(self, item:ITEMSTYPE=None):
        """ Supprime un Effet, Elément, Race du set() des items correspondants.
            paramètre:
                item :  choix de type ITEMSTYPE à supprimer du set(). Si la liste devient
                        vide, ajoute l'élément ' ... '. 
        """
        elide:dict = {"Effets":" l'effet ","Eléments":" l'élément ","Races":" la race "}
        getitem = self.typeItems_Dico[item][0].get()
        self.typeItems_Dico[item][1].discard(getitem)
        if not (self.typeItems_Dico[item][1] & set({""," ... ","None"})):
            self.state_bar.update_vltexte(f" Info : Suppression de{elide[item]}'{getitem}' à la liste des effets effectuée.", 3)
        if not self.typeItems_Dico[item][1]: self.typeItems_Dico[item][1].add(' ... ')
        self.__list_items__(item=item, update=True)
    
    def specificFrame(self, event:tk.Event=None):
        """ Méthode de gestion dynamique d'affichage des widgets qui est déclenchée
            par l'évènement virtuel "<<ComboboxSelected>>"  lors de la sélection
            du type de carte 'créature', 'evenement', 'spell' ou 'terrain'.
        """
        backup_race = self.frameBackuplistes.nametowidget("!chkbtnBackupRace")
        label_typecreature = self.frameCardDB.nametowidget('!labelTypeCreature')
        colordico:dict = {"equipement":"#E9FAD8","spell":"#D8E6FA","terrain":"#F3D6B6"}
        elidedico:dict = {"creature":" de la ","equipement":" de l'","spell":" de la carte ","terrain":" du "}
        # ----- liste des noms des widgets du coût et monnaies des cartes ----- 
        cost_widgets = [self.frameCardDB.nametowidget(widget) for widget in \
                                    list(filter(lambda name:"Cost" in name,self.frameCardDB.children.keys()))]
        # ---------------------------------------------------------------------
        w = event.widget if event else self.comboxCardType
        if w.get() not in ["creature","terrain"]:
            if w.get() != 'Spell':
                label_typecreature.configure(state="disabled")
                self.comboxRaceType.configure(state="disabled")
            # -----------------------------------------------------------------
            self.vtypetarget.set(self.typetargetlist[-1])
            # ------- recherche des frames spécifiques pour les masquer -------
            frames_to_remove = set(filter(lambda lf: w.get() not in lf.name(), self.framelist))
            #print(f"frames_to_remove: {frames_to_remove}")
            for remove_frame in frames_to_remove: remove_frame.grid_remove() 
            # ----- 'NON ET' des set() pour obtention la frame à afficher -----
            grid_frame = list(self.framelist - frames_to_remove)[0]
            label = f" Attribut spécifique au type de carte '{w.get()}'"
            grid_frame.configure(bg=colordico[w.get()],text=label,font=self.frmfont)
            grid_frame.grid()
        else:
            # ------ Dévalidation widgets 'coût' et 'typecreature'si carte terrain ------    
            if w.get() == "terrain":
                label_typecreature.configure(state="disabled")
                [widget.configure(state="disabled") for widget in cost_widgets]
            else:
                label_typecreature.configure(state="normal")
                self.vtypetarget.set(self.typetargetlist[0])
                self.comboxRaceType.configure(state="readonly")
            [frame.grid_remove() for frame in self.framelist]
        # ---------- changement d'état du tk.CheckButton() des Races ----------
        backup_race.configure(state="normal" if w.get() == "equipement" else "disabled")
        # ------- remise des 'cost_widget' à l'état 'normal'/'readonly' -------
        if cost_widgets[0].cget("state") == "disabled" and w.get() != 'terrain':
                [widget.configure(state="normal" if not isinstance(widget, ttk.Combobox) \
                                                      else 'readonly') for widget in cost_widgets]
        # ---------------------------------------------------------------------
        dummy_name = f" Nom{elidedico[w.get()]}{w.get()}"            
        self.vlabelname.set(f"{dummy_name:<22} :")

    def load_CARDDB_file(self):
        files = os.listdir(Card.CardDBOutPath)
        title = "Choix du fichier CardDB à lire"
        cardtypes = [("Cartes CardDB", "*.json"),("Tous les fichiers", "*"),]
        dummyFile = askopenfilename(title=title,initialfile=files[0],initialdir=Card.CardDBOutPath,
                                            filetypes=cardtypes,parent=self,typevariable=self.vcardDBFname)
        if dummyFile:
            try:
                cardtype, name = osp.basename(dummyFile).split('.')[0].split('_',maxsplit=1)
                self.__load_cardDB_card(readFile(name, cardtype))
            except ValueError as msg:
                self.state_bar.update_vltexte(f" Info : Incompatibilité de données lors de la lecture du fichier {osp.basename(dummyFile)}" )
                
    def __load_cardDB_card(self, cardDB:Creature|Equipment|Spell|Terrain):
        self.__raz_default()
        self.vmastertitle.initialize(" Type de carte à modifier :")        
        # --------------------------- Fichier Image ---------------------------
        self.vcardimageFname.set(osp.basename(cardDB.imageFilename))
        # ---------------------------------------------------------------------
        self.vname.set(cardDB.name)
        self.vcardtype.set(cardDB.cardType)
        if self.vcardtype.get() != "terrain":
            self.vcost.set(cardDB.cost)
            self.vraces.set('None') if cardDB.cardType != 'creature' else cardDB.race
            self.vcurencytype.set(cardDB.currency)
            self.vracesequip.set(cardDB.race) 
            self.vtalentstype.set(cardDB.talent)
            self.varmes.set(cardDB.weaponType)
            [self.multielementlist.add(element) for element in cardDB.elementType] if cardDB.elementType else self.multielementlist.add('None')
            self.velementstype.set(list(self.multielementlist)[0])
            [self.multieffetlist.add(effet) for effet in cardDB.effects] if cardDB.effects else self.multieffetlist.add('None')
            self.veffects.set(list(self.multieffetlist)[0])
            self.vhp.set(cardDB.combatStat.hp)
            self.vheal.set(cardDB.combatStat.heal)
            self.vatk.set(cardDB.combatStat.atk)
            self.vdef.set(cardDB.combatStat.defense)
            self.vtypecrit.set(cardDB.combatStat.crit)
            self.vtypetarget.set(cardDB.combatStat.target)
            # ---------------------------------------------------------------------
            match self.vcardtype.get():
                case "equipement":
                    self.vitemtype.set(cardDB.equipmentType)
                    self.varmesequip.set(cardDB.weaponType)
                    [self.multiracequiplist.add(race) for race in cardDB.race] if cardDB.race else self.multiracequiplist.add('None')
                    self.vracesequip.set(list(self.multiracequiplist)[0])
                    self.__valide_armequipement()
                case "spell":
                    self.vtypesort.set(cardDB.typeSort)
        else:
            [self.multieffetlist.add(effet) for effet in cardDB.effects] if cardDB.effects else self.multieffetlist.add('None')
            self.veffects.set(list(self.multieffetlist)[0])
        # ---------- chargement et affichage de l'image de la carte -----------
        self.newImage = self.preload_cardDB_Image(osp.basename(self.vcardimageFname.get()))
        if self.newImage:
            self.cardDBcanvas.itemconfigure(self.cardDB_image, image = self.newImage)
        # ---- mise à jour de la frame spécicifique à chaque type de carte ----           
        self.specificFrame()

    def __save_CARDDB_card(self):
        ok = False
        typecard = self.vcardtype.get()
        self.MessageBox.boxtitle(f"Création carte '{typecard}'")
        match typecard:
            case 'creature':
                try:
                    typecard, name = osp.basename(self.__save_creature()).split('_',maxsplit=1)
                    ok = True
                except ValueError as msg:
                    self.MessageBox.message = msg    
            case 'equipement':
                try:
                    typecard, name = osp.basename(self.__save_equipement()).split('_',maxsplit=1)
                    ok = True
                except ValueError as msg:
                    self.MessageBox.message = msg    
            case 'spell':
                try:
                    typecard, name = osp.basename(self.__save_spell()).split('_',maxsplit=1)
                    ok = True
                except ValueError as msg:
                    self.MessageBox.message = msg    
            case 'terrain':
                try:
                    typecard, name = osp.basename(self.__save_terrain()).split('_',maxsplit=1)
                    ok = True
                except ValueError as msg:
                    self.MessageBox.message = msg    
        if not ok:
            self.state_bar.update_vltexte(f" Info : Carte '{self.vcardtype.get()}' non crée, erreur de données pour la carte demandée")
        else:  
            # -- raz listes talents, races ... et variables si sauvegarde ok --
            self.state_bar.update_vltexte(f" Info : Carte {typecard} '{name}' sauvegardée avec succès")
            self.__raz_default()
    
    def __save_terrain(self) -> str:
        # ------------------- création de l'objet 'terrain' -------------------
        terrain_card = Terrain(name=self.vname.get(),
                               effects=[item for item in self.get_items("Effets") if item not in (" ... ","None")],
                               )
        terrain_card.imageFilename = osp.join("./",Card.ImageOutPath,self.vcardimageFname.get())
        return writeFile(terrain_card, overwrite=True)
                        
    def __save_spell(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        spell_card = Spell( name=self.vname.get(),
                            cost=self.vcost.get(),
                            currency=self.vcurencytype.get(),
                            typeSort=self.vtypesort.get(),
                            hp=self.vhp.get(),
                            crit=self.vtypecrit.get(),
                            atk=self.vatk.get(),
                            defense=self.vdef.get(),
                            heal=self.vheal.get(),
                            target=self.vtypetarget.get(),
                            race=self.vraces.get(),
                            weaponType=self.varmes.get(),
                            effects=self.get_items("Effets"),                                 
                            talent=self.vtalentstype.get(),
                            elementType=self.get_items("Eléments"),
                           )
        spell_card.imageFilename = osp.join("./",Card.ImageOutPath,self.vcardimageFname.get())
        return writeFile(spell_card,overwrite=True)
                    
    def __save_equipement(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        equipement_card = Equipment(weaponType=self.varmesequip.get(),
                                    elementType=self.get_items("Eléments"),
                                    itemType=self.vitemtype.get(),
                                    name=self.vname.get(),
                                    cost=self.vcost.get(),
                                    currency=self.vcurencytype.get(),
                                    hp=self.vhp.get(),
                                    crit=self.vtypecrit.get(),
                                    atk=self.vatk.get(),
                                    defense=self.vdef.get(),
                                    heal=self.vheal.get(),
                                    target=self.vtypetarget.get(),
                                    effects=self.get_items("Effets"),                                 
                                    talent=self.vtalentstype.get(),
                                    race=self.get_items("Races"),
                                    )
        equipement_card.imageFilename = osp.join("./",Card.ImageOutPath,self.vcardimageFname.get())
        return writeFile(equipement_card,overwrite=True)
    
    def __save_creature(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        creature_card = Creature(race=self.vraces.get(),
                                 elementType=self.get_items("Eléments"),
                                 name=self.vname.get().strip().capitalize(),
                                 cost=self.vcost.get(),
                                 currency=self.vcurencytype.get(),
                                 hp=self.vhp.get(),
                                 crit=self.vtypecrit.get(),
                                 atk=self.vatk.get(),
                                 defense=self.vdef.get(),
                                 heal=self.vheal.get(),
                                 target=self.vtypetarget.get(),
                                 weaponType=self.varmes.get(),
                                 effects=self.get_items("Effets"),                                 
                                 talent=self.vtalentstype.get(),
                                 )
        creature_card.imageFilename = osp.join("./",Card.ImageOutPath,self.vcardimageFname.get())
        return writeFile(creature_card,overwrite=True)

    def get_combobox(self, itemtype:ITEMSTYPE) -> ttk.Combobox:
        match itemtype:
            case "Effets"   : combobox = self.effetsCombobox
            case "Races"    : combobox = self.racesEquipCombobox
            case "Eléments" : combobox = self.elementsCombobox
            case "Talents"  : combobox = self.talentsCombobox    
        return combobox
    
    def __toggle_backupList(self):
        self.__saveItemsList_onQuit = not self.__saveItemsList_onQuit
        if not self.__saveItemsList_onQuit:
            self.backup_bar.update_vltexte("",0)
        else:
            self.backup_bar.update_vltexte(" Sauvegarde des listes déroulantes Activée",1)
            
        print(f"self.__saveItemsList_onQuit: {self.__saveItemsList_onQuit}")

    def __update_backupStateBar(self, itemtype:ITEMSTYPE, mode:int):
        """ Méthode de mise à jour du message de la 'backup_StateBar' qui 
            donne les listes déroulantes qui seront sauvegardées.
        """
        str_items = ", ".join([item for item in self.items_dico.keys() if self.cbox_textvariable_dico[item].get()])
        if self.__saveItemsList_onQuit:
            self.backup_bar.update_vltexte(f" Sauvegarde de: {str_items}",1)

    def __get_ItemFromCboxName(self, comboboxName:str) -> ITEMSTYPE:
        """ Méthode qui renvoi le nom de type ITEMSTYPE d'après le 'ttk.Combobox._name'
            passé en paramètre 
            Paramètre:
                comboboxname : attribut '_name' d'une ttk.Combobox 
        """
        Items_dico:dict = {"effets":"Effets","races":"Races","elements":"Eléments","talents":"Talents"}
        return Items_dico.get(sub(r'!|Combobox',"",comboboxName).strip(), None)
        
    def __update_ComboboxState(self, itemtype:ITEMSTYPE|None=None):
        """ Méthode qui change le status des tk.Combobox() pour pouvoir ajouter
            des items à la liste des 'values' du widget. et mise à jour du
            message de la 'backup_StateBar'.
        """
        self.get_combobox(itemtype).configure(state="normal" \
                            if self.cbox_textvariable_dico[itemtype].get()==1 else "readonly")  
        self.__update_backupStateBar(itemtype, self.cbox_textvariable_dico[itemtype].get())    

    def __delete_comboboxValues(self, event:tk.Event=None):
        """ Méthode callback de l'évènement virtuel '<<ComboboxDelItem>>'. Permet de
            supprimer un élément de la liste des valeurs de la Combobox appelante.
        """
        if event and isinstance(event.widget, ttk.Combobox):
            w = event.widget
            item = self.__get_ItemFromCboxName(w._name)
            if all([item, self.cbox_textvariable_dico.get(item, False).get()]):
                values = list(w.cget('values'))
                if w.select_present() and w.selection_get() == values[w.current()]:
                    print(f"\tw.selection_get(): {w.selection_get()}\n\tvalues[w.current(): {values[w.current()]}")
                    values.pop(w.current())
                    w.configure(values=values)
            else:
                return 'break'

    def __update_comboboxValues(self, event:tk.Event=None):
        """ Méthode callback de l'évènement virtuel '<<ComboboxAddItem>>'. Permet d'ajouter
            un élément à la liste des valeurs de la Combobox appelante.
        """
        if event and isinstance(event.widget, ttk.Combobox):
            w = event.widget
            item = self.__get_ItemFromCboxName(w._name)
            if all([item, self.cbox_textvariable_dico.get(item, None).get()]):
                self.__update_comboboxList__(itemtype=item, combobox=w)
            else:
                return 'break'

    def __update_comboboxList__(self, itemtype:ITEMSTYPE, combobox:ttk.Combobox):
        """ Méthode de mise à jour de la liste de la Combobox() référencée par 'itemtype' """
        items = set()
        [items.add(item) for item in list(combobox.cget('values'))+[combobox.get(),] if item]
        combobox.configure(values=list(items))

    def __backup_etea_list(self):
        """ Méthode de sauvegarde des listes des Combobox() si la variable
            'self.__saveItemsList_onQuit' est sur 'True' et si la variable 
            de controle de l'item est à 1 (True). 
        """
        for item in self.typeItems_Dico:
            # ---- comparaisons des variables des tk.Checkbox() de backup -----
            if bool(self.cbox_textvariable_dico[item].get()):
                # ------ génération du nom de fichier fonction de l'item ------
                filename = osp.join("./","coreDataDB","".join([c.lower().replace('é','e') for c in item]))
                # ------ recherche des 'values' de la combobox de l'item ------
                items_list = list(self.get_combobox(item).cget('values'))
                # --- Ecriture du fichier 'Items' avec les nouvelle valeurs ---               
                with open(filename, mode="w", encoding='utf-8') as itemfile:
                    itemfile.writelines(f"{line}\n" for line in items_list)
            
    def __toggle_fullscreen(self, event:tk.Event=None):
        self.state("normal" if self.state() == "zoomed" else "zoomed")
    
    def __exit_fullscreen(self, event:tk.Event=None):
        self.state("normal")
                    
    def fenetre_a_propos(self, event:tk.Event=None):
        """ Fenêtre-message à propos.
            Indique le nom du/des auteurs ainsi que la/les licences.
        """
        message = "CARDDB GUI v1.5"+"\n\nCopyright (C) 2026\nBernard Amouroux" \
        "\nLicense : GPL Version 3, 29 June 2007\n" \
        "\nMoteur du support de création des cartes"+"\nJan Amouroux" \
        "\nLicense : GPL Version 3, 29 June 2007\n" \
        "\nSur une Idée originale de\nDoriqam Vidal  et  Lecurieux Stevens\n"
        self.MessageBox.textfont('Times 15 normal roman')
        self.MessageBox.boxtitle('À propos')
        self.MessageBox.message = message
    
    def Quit(self):
        if self.__saveItemsList_onQuit:
            self.backup_bar.update_vltexte(" Sauvgarde en cours ...")
            self.__backup_etea_list()    
            self.after(1000, self.destroy)
        else:
            self.destroy()    
        
        
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
        icon = tk.PhotoImage(master=app, file=osp.join(os.getcwd(),'imgsDataDB','carddb.png'))
        app.wm_iconphoto(True, icon)
    # -------------------------------------------------------------------------
    app.title("CARDDB GUI v1.5 (c)2026 AMOUROUX Bernard - GUI de saisie des cartes de CARDDB (c)2026 AMOUROUX Jan")
    app.mainloop()
        