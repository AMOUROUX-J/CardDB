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

import locale
import os, sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path as osp

from main import writeFile
from SpellCard import Spell
from TerrainCard import Terrain
from equipmentCard import Equipment
from CreatureCard import Creature
from cardLogics import readRules
from tkinter.font import Font


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
    def __init__(self, master:tk.Tk, message:str=None, msgtext=('Consolas 11 bold italic'), *args, **kwargs):
        """ Attributs du constructeur: 
                master : objet tkinter.Tk() ou tkinter.Toplevel()
                message (str): texte qui sera affiché dans la fenètre
                msgtext : police de caractères des messages d'information
        """    
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
   

class Application(tk.Tk):
    
    def __init__(self):
        
        tk.Tk.__init__(self, className = "Tk", useTk = True)

        self.MessageBox = Win_MessageBox(self)  
        self.state_bar = Window_StateBar(self,"",0,0,10,cspan=20,bg='tan',pady=3,txtfont=('Consolas 10 bold italic'))                                         
        self.state_bar.message = " Info : Appuyez sur 'F1' pour la fenètre 'A propos'"

        self.ttlfont = Font(self, family='Courier',size=14,weight='bold',slant='italic')
        self.lblfont = Font(self, family='Consolas',size=10,weight='bold',slant='italic')
        self.itemfont= Font(self, family='Courier New',size=12,weight='bold',slant='italic')
        self.cmbfont = Font(self, family='Consolas',size=16,weight='normal',slant='italic')
        self.frmfont = Font(self, family="Times", size=12, weight="bold", slant="roman")
        
        # ---------------------------------------------------------------------
        self.protocol('WM_DELETE_WINDOW',self.Quit)
        # ---------------------------------------------------------------------
        self.bind('<F1>', self.fenetre_a_propos)
        self.columnconfigure(list(range(20)), minsize=40, weight=1)
        self.rowconfigure(list(range(11)), minsize=32, weight=0)
        self.minsize(width=800, height=380)
        self.anchor('nw')
        
        self.init_variables()
        self.cree_widgets()
    
    def init_variables(self):
        """ Définition de toutes les variables de type tkinter.StringVar() ou tkinter.Inrvar()
            utilisées par l'application.
        """
        self.cardtypelist:list = ["creature", "equipement", "spell", "terrain"]
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
        self.vracesequip = tk.StringVar(value=["None",])
        self.multiracelist = set()
        self.typeffetlist = readRules('effets') 
        self.vterraineffet = tk.StringVar(value=self.typeffetlist[-1])
        self.multieffetlist = set()
        # ---------------------------------------------------------------------
        self.multiSetlist = [self.multiracelist, self.multitalentlist, self.multielementlist, self.multieffetlist] 
        # ---------------------------------------------------------------------
        self.vname = tk.StringVar()
        self.vlabelname = tk.StringVar(value=" Nom de la créature à créer :")
        self.vcost = tk.IntVar(value=1)
        self.vhp = tk.IntVar(value=10)
        self.vheal = tk.IntVar(value=0)
        self.typecritlist:list = [0,2,6,8,20]
        self.vtypecrit = tk.IntVar(value=self.typecritlist[0])
        self.typetargetlist:list = ["mono","zone","groupe",None]
        self.vtypetarget = tk.StringVar(value=self.typetargetlist[0]) 
        self.vatk = tk.IntVar(value=0)
        self.vdef = tk.IntVar(value=0)
    
    def cree_widgets(self):
        """ Création de tous les widgets de la fenètre principale
            Configuration et affichage/masquage des widgets en dynamique (gestion des évènements)
        """
        globalframe = My_LabelFrame(self,cspan=20,rspan=9,pad=(2,2,2,2),sticky="nsew")
        # ---------------------------------------------------------------------
        titleframe = My_LabelFrame(globalframe,col=2,row=0,cspan=16,bg="#FBE6C8",pad=(2,2,0,0),sticky="ew")
        tk.Label(titleframe,text=" Type de carte à créer :",bg=titleframe.cget('bg'),
                                      font=self.ttlfont).grid(column=0,row=0,columnspan=8,sticky="new")
        self.comboxCardType = ttk.Combobox(titleframe,background=titleframe.cget('bg'),
                                    font=self.cmbfont,postcommand=None,values=self.cardtypelist,
                                             state="readonly",name="!comboxCardType",textvariable=self.vcardtype)
        self.comboxCardType.grid(column=8,row=0,columnspan=8,sticky="new")
        self.comboxCardType.bind("<<ComboboxSelected>>",self.specificFrame)
        # ---------- frame des attributs communs à toutes les carte -----------
        self.framenom = My_LabelFrame(globalframe,col=0,row=1,cspan=20,bg=globalframe.cget('bg'),
                                          name="!labelFramenom",pad=(2,0,0,0),bd=1,relief="solid",sticky="new")
        tk.Label(self.framenom,bg=self.framenom.cget('bg'),textvariable=self.vlabelname,
                            anchor="w",font=self.itemfont).grid(row=0,column=0,columnspan=4,pady=4,sticky="nw")
        tk.Entry(self.framenom,bg='ivory',textvariable=self.vname,
                            font=self.itemfont).grid(column=4,columnspan=3,row=0,pady=4,ipady=1,sticky="nw")
        tk.Label(self.framenom,bg=self.framenom.cget('bg'),text="Type de créature :",name="!labelTypeCreature",
                            anchor="w",font=self.itemfont).grid(row=0,column=7,columnspan=4,pady=4,sticky="nw")
        self.comboxRaceType = ttk.Combobox(self.framenom,background=self.framenom.cget('bg'),
                                      font=self.itemfont,postcommand=None,values=self.raceslist,
                                          state="readonly",name="!comboxRacesType",textvariable=self.vraces)
        self.comboxRaceType.grid(column=12,row=0,columnspan=8,pady=4,sticky="nw")
        
        # ---------------------------------------------------------------------
        framecost = My_LabelFrame(globalframe,col=0,row=2,cspan=10,bg=globalframe.cget('bg'),
                                                                         bd=1,relief="solid",sticky="new") 
        tk.Label(framecost,text=" Coût de la carte      :",bg=framecost.cget('bg'),
                               font=self.itemfont).grid(row=0,column=0,columnspan=4,pady=4,sticky="nw")
        tk.Entry(framecost,bg='ivory',textvariable=self.vcost,width=3,
                                  font=self.itemfont).grid(column=4,row=0,columnspan=2,pady=4,sticky="n")
        self.curencyCombobox = ttk.Combobox(framecost,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=self.curencytypelist,
                                                state="readonly",name="!curencyCombobox",textvariable=self.vcurencytype)
        self.curencyCombobox.grid(column=6,row=0,columnspan=4,padx=2,pady=4,sticky="new")
        # ---------------------------------------------------------------------
        frametalents = My_LabelFrame(globalframe,col=10,row=2,cspan=10,rspan=6,bg=globalframe.cget('bg'),
                                                                        pad=(2,0,0,0),bd=1,relief="solid",sticky="new") 
        tk.Label(frametalents,text=" Talent(s)  :",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=0,column=0,columnspan=3,pady=4,sticky="nw")
        self.talentsCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=self.talentstypelist,
                                                state="readonly",name="!talentsCombobox",textvariable=self.vtalentstype)
        self.talentsCombobox.grid(column=3,row=0,columnspan=7,padx=8,pady=4,sticky="new")
        tk.Button(frametalents,text="Ajouter à la liste des talents",font=self.lblfont,
                                        command=self.__add_talent).grid(column=0,row=1,columnspan=10,padx=3,sticky="ew")
        tk.Label(frametalents,text=" Elément(s) :",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=2,column=0,columnspan=3,pady=4,sticky="nw")
        self.elementsCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=list(self.elementstypelist),
                                                state="readonly",name="!elementsCombobox",textvariable=self.velementstype)
        self.elementsCombobox.grid(column=3,row=2,columnspan=7,padx=8,pady=4,sticky="new")
        tk.Button(frametalents,text="Ajouter à la liste des éléments",font=self.lblfont,
                                        command=self.__add_element).grid(column=0,row=3,columnspan=10,padx=3,sticky="ew")
        tk.Label(frametalents,text=" Arme équipable : ",bg=frametalents.cget('bg'),
                               font=self.itemfont).grid(row=4,column=0,columnspan=3,pady=4,sticky="nw")
        self.armesCombobox = ttk.Combobox(frametalents,background=globalframe.cget('bg'),
                                            font=self.itemfont,postcommand=None,values=list(self.armeslist),
                                                state="readonly",name="!armesCombobox",textvariable=self.varmes)
        self.armesCombobox.grid(column=3,row=4,columnspan=6,padx=2,pady=4,sticky="new")
        # ---------------------------------------------------------------------
        texte = " Données statistiques de combat "
        frameproperty = My_LabelFrame(globalframe,col=0,row=3,cspan=10,rspan=3,bd=2,bg=globalframe.cget('bg'),
                                               font=self.lblfont,text=texte,pad=(0,7,0,0),relief="ridge",sticky="new")  
        tk.Label(frameproperty,text=" Points de vie   :",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=0,column=0,columnspan=3,pady=4,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vhp,width=3,
                                  font=self.itemfont).grid(column=3,row=0,columnspan=1,pady=4,sticky="nw")
        tk.Label(frameproperty,text=" Santé   : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=0,column=4,columnspan=1,pady=4,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vheal,width=3,
                                  font=self.itemfont).grid(column=5,row=0,columnspan=1,pady=4,sticky="nw")
        tk.Label(frameproperty,text=" Points d'attaque:",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=1,column=0,columnspan=3,pady=4,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vatk,width=3,
                                  font=self.itemfont).grid(column=3,row=1,columnspan=1,pady=4,sticky="nw")
        tk.Label(frameproperty,text=" Points de défense :",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=1,column=4,columnspan=3,pady=4,sticky="nw")
        tk.Entry(frameproperty,bg='ivory',textvariable=self.vdef,width=3,
                                  font=self.itemfont).grid(column=7,row=1,columnspan=1,pady=4,sticky="nw")
        tk.Label(frameproperty,text=" Valeur de crit. :",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=2,column=0,columnspan=3,pady=4,sticky="nw")
        ttk.Spinbox(frameproperty,background='ivory',command=None,font=self.itemfont,
                                      values=self.typecritlist,width=3,textvariable=self.vtypecrit,
                                            state="readonly",wrap=True).grid(column=3,row=2,pady=4,sticky="nw")
        tk.Label(frameproperty,text=" Cible   : ",bg=frameproperty.cget('bg'),
                               font=self.itemfont).grid(row=2,column=4,columnspan=1,pady=4,sticky="nw")
        self.targetCombobox = ttk.Combobox(frameproperty,background=globalframe.cget('bg'),width=10,
                                            font=self.itemfont,postcommand=None,values=list(self.typetargetlist),
                                                state="readonly",name="!elementsCombobox",textvariable=self.vtypetarget)
        self.targetCombobox.grid(column=5,row=2,columnspan=5,padx=2,pady=4,sticky="new")
        # ---------------------------------------------------------------------
        texte = f" Aucun attribut spécifique pour les cartes de type '{self.comboxCardType.get()}' "
        framecreature = My_LabelFrame(globalframe,col=0,row=6,cspan=20,rspan=2,font=self.frmfont,text=texte)
        tk.Label(framecreature,text=f" ",bg=framecreature.cget('bg'),
                                               font=self.frmfont).grid(column=0,row=0,columnspan=20,sticky="nsew")
        # ----------- frame des attributs spécifiques à Equipement ------------
        self.equipementFrame = My_LabelFrame(globalframe,col=0,row=6,cspan=20,rspan=2,
                                                                  bg="#E9FAD8",name="!equipementFrame",sticky="sew")
        tk.Label(self.equipementFrame,anchor="w",bg=self.equipementFrame.cget('bg'),text=" Mode de défense :",
                                                    font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="w")
        self.equipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                        font=self.itemfont,postcommand=None,values=self.itemtypelist,
                                             state="readonly",name="!equipementCombobox",textvariable=self.vitemtype)
        self.equipCombobox.grid(column=2,row=0,columnspan=4,pady=2,sticky="w")
        tk.Label(self.equipementFrame,text=" Type d'arme :",bg=self.equipementFrame.cget('bg'),
                               font=self.itemfont).grid(row=1,column=0,columnspan=2,sticky="w")
        self.armesEquipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                            font=self.itemfont,postcommand=None,values=list(self.armeslist),
                                                state="readonly",name="!armesCombobox",textvariable=self.varmesequip)
        self.armesEquipCombobox.grid(column=2,row=1,columnspan=4,pady=2,sticky="w")
        self.armesEquipCombobox.set(self.armeslist[2])
        tk.Label(self.equipementFrame,text=" Races équipées :",bg=self.equipementFrame.cget('bg'),
                               font=self.itemfont).grid(row=0,column=6,columnspan=6,sticky="w")
        self.racesEquipCombobox = ttk.Combobox(self.equipementFrame,background=self.equipementFrame.cget('bg'),
                                        font=self.itemfont,postcommand=None,values=list(self.raceslist),
                                                state="readonly",name="!racesCombobox",textvariable=self.vracesequip)
        self.racesEquipCombobox.grid(column=12,row=0,columnspan=8,pady=2,sticky="w")
        tk.Button(self.equipementFrame,text="Ajouter à la liste des races",font=self.lblfont,
                                        command=self.__add_race).grid(column=6,row=1,columnspan=14,padx=3,sticky="ew")
        # -------------- frame des attributs spécifiques à Sort ---------------
        self.spellFrame = My_LabelFrame(globalframe,col=0,row=6,cspan=20,rspan=2,bg="#D8E6FA",name="!spellFrame",sticky="sew")
        tk.Label(self.spellFrame,anchor="center",bg=self.spellFrame.cget('bg'),text=f"{' Type de sort :':>20}",
                                              font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="w")
        self.spellCombobox = ttk.Combobox(self.spellFrame,background=self.spellFrame.cget('bg'),
                                        font=self.itemfont,postcommand=None,values=self.typesortlist,
                                             state="readonly",name="!spellCombobox",textvariable=self.vtypesort)
        self.spellCombobox.grid(column=2,row=0,columnspan=4,pady=2,sticky="w")
        # ------------ frame des attributs spécifiques au terrain -------------
        self.terrainFrame = My_LabelFrame(globalframe,col=0,row=6,cspan=20,rspan=2,bg="#F3D6B6",name="!terrainFrame",sticky="sew")
        tk.Label(self.terrainFrame,anchor="center",bg=self.terrainFrame.cget('bg'),text=f"{' Type d\'effet :':>20}",
                                              font=self.itemfont).grid(row=0,column=0,columnspan=2,sticky="w")
        self.terrainCombobox = ttk.Combobox(self.terrainFrame,background=self.terrainFrame.cget('bg'),
                                        font=self.itemfont,postcommand=None,values=self.typeffetlist,
                                             state="readonly",name="!terrainCombobox",textvariable=self.vterraineffet)
        self.terrainCombobox.grid(column=2,row=0,columnspan=4,pady=2,sticky="w")
        tk.Button(self.terrainFrame,text="Ajouter à la liste des effets",font=self.lblfont,
                                        command=self.__add_effet).grid(column=6,row=0,columnspan=14,padx=3,sticky="ew")
        # ----------------- frame buttons save/default/cancel -----------------
        buttonFrame = My_LabelFrame(self,col=0,row=9,cspan=20,pad=(2,0,0,3))
        tk.Button(buttonFrame,text=" RàZ Défaut ",bg="#FDEED0",command=self.__raz_default,
                                            font=self.frmfont).grid(column=3,row=0,columnspan=2,sticky="ew")
        tk.Button(buttonFrame,bg="#C9FFD3",font=self.frmfont,command=self.save_CARDDB_card,
                                text=" Enregistrer la carte ").grid(column=9,row=0,columnspan=2,sticky="ew")
        tk.Button(buttonFrame,text=" Annuler/Quitter ",command=self.Quit,bg="#FCC6C6",
                                           font=self.frmfont).grid(column=15,row=0,columnspan=2,sticky="ew")
        # ---------------------------------------------------------------------
        self.framelist = set({self.equipementFrame,self.spellFrame,self.terrainFrame})
        self.comboxCardType.event_generate("<<ComboboxSelected>>")
        self.state_bar.update_vltexte("",0)
        # ---------------------------------------------------------------------
    
    def __raz_default(self):
        self.vtypetarget.set('mono') if self.vcardtype.get()=="creature" else self.vtypetarget.set('None')
        self.velementstype.set('None'); self.vtalentstype.set('None'); self.varmes.set('None')
        self.vracesequip.set('None'); self.vterraineffet.set('None')
        self.__clear_multisetlist__()
    
    def __clear_multisetlist__(self):
        """ RAZ des listes de self.multiSetlist """
        [setlist.clear() for setlist in self.multiSetlist]
        #[print(setlist) for setlist in self.multiSetlist] 
        
    def __add_effet(self, event:tk.Event=None):
        if not self.vterraineffet.get() == 'None':
            self.multieffetlist.add(self.vterraineffet.get())         
        print(f"self.multieffetlist: {self.multieffetlist}")
    
    def get_effets(self) -> list:
        return list(self.multieffetlist)    
    
    def __add_talent(self, event:tk.Event=None):
        """ Méthode privée de création du set() des talents """
        if not self.vtalentstype.get() == 'None':
            self.multitalentlist.add(self.vtalentstype.get())
        #print(f"self.multitalentlist: {self.multitalentlist}")
    
    def get_talents(self) -> list:
        """ Retourne la liste des 'talents' par conversion en list() """
        return list(self.multitalentlist)           
    
    def __add_element(self, event:tk.Event=None):
        """ Méthode privée de création du set() des éléments """
        if not self.velementstype.get() == 'None':
            self.multielementlist.add(self.velementstype.get())         
        #print(f"self.multielementlist: {self.multielementlist}")
    
    def get_elements(self) -> list:
        """ Retourne la liste des 'elements' par conversion en list() """
        return list(self.multielementlist)                 

    def __add_race(self, event:tk.Event=None):
        """ Méthode privée de création du set() des races des équipements """
        self.multiracelist.add(self.vracesequip.get())
        self.multiracelist.discard('None')
        #print(f"self.multiracelist: {self.multiracelist}")
        
    def get_races(self) -> list:
        """ Retourne la liste des 'races équipables' par conversion en list() """
        return list(self.multiracelist)                 

    def specificFrame(self, event:tk.Event=None):
        """ Méthode de gestion dynamique d'affichage des widgets qui est déclenchée
            par l'évènement virtuel "<<ComboboxSelected>>" émis lors de la sélection
            du type de carte 'créature', 'evenement' ou 'spell'.
        """
        label_typecreature = self.framenom.nametowidget('!labelTypeCreature')
        colordico:dict = {"equipement":"#E9FAD8","spell":"#D8E6FA","terrain":"#F3D6B6"}
        elidedico:dict = {"creature":" de la ","equipement":" de l'","spell":" de la carte ","terrain":" du "}
        w = event.widget if event else self.comboxCardType
        if w.get() != "creature":
            label_typecreature.configure(state="disabled")
            self.comboxRaceType.configure(state="disabled")
            self.vtypetarget.set(self.typetargetlist[-1])
            frame_to_remove = set(filter(lambda lf: w.get() not in lf.name(), self.framelist))
            for remove_frame in frame_to_remove:
                #print(f"specificFrame(remove_frame): {remove_frame}")
                remove_frame.grid_remove() 
                # -------------------------------------------------------------
            grid_frame = list(self.framelist - frame_to_remove)[0]
            #(f"specificFrame(grid_frame): {grid_frame}")
            label = f" Attribut spécifique au type de carte '{w.get()}'"
            grid_frame.configure(bg=colordico[w.get()],text=label,font=self.frmfont)
            grid_frame.grid()
        else:
            label_typecreature.configure(state="normal")
            self.vtypetarget.set(self.typetargetlist[0])
            self.comboxRaceType.configure(state="normal")
            [frame.grid_remove() for frame in self.framelist]
        dummy_name = f" Nom{elidedico[w.get()]}{w.get()}"            
        self.vlabelname.set(f"{dummy_name:<22} :")

    def __valid_CARDDB_card__(self) -> bool:
        if not self.vname.get() or len(self.vname.get()) < 2:
            return False
        if not self.vcost.get() > 0:
            return False
        return True
    
    def __valid_terrain(self) -> bool:
        if self.__valid_CARDDB_card__():
            if not self.get_effets() or self.vterraineffet.get() == "None":
                return False
            return True
        return False  
        
    def __valid_spell(self) -> bool:
        if self.__valid_CARDDB_card__():
            if self.varmes.get() == "None":
                return False
            if not self.get_elements() or self.velementstype.get() == "None":
                return False
            return True
        return False  

    def __valid_creature(self) -> bool:
        if self.__valid_CARDDB_card__():
            if self.vraces.get() == None:
                return False
            if not self.get_elements():
                return False
            return True
        return False
    
    def __valid_equipement(self) -> bool:
        if self.__valid_CARDDB_card__():
            if self.varmesequip.get() == "None":
                return False
            if not self.get_elements() or self.velementstype.get() == "None":
                return False 
            if not self.multiracelist:
                return False
            if self.vtypetarget.get() == 'None':
                return False
            return True        
        return False
    
    def save_CARDDB_card(self):
        ok = False
        match self.vcardtype.get():
            case 'creature':
                if self.__valid_creature():
                    typecard, name = osp.basename(self.__save_creature()).split('_')
                    ok = True
            case 'equipement':
                if self.__valid_equipement():
                    typecard, name = osp.basename(self.__save_equipement()).split('_')
                    ok = True
            case 'spell':
                if self.__valid_spell():
                    typecard, name = osp.basename(self.__save_spell()).split('_')
                    ok = True
            case 'terrain':
                if self.__valid_terrain():
                    typecard, name = osp.basename(self.__save_terrain()).split('_')
                    ok = True
        if not ok:
            self.state_bar.update_vltexte(f" Info : Carte '{self.vcardtype.get()}' non crée, incompatibilité de données pour la carte demandée")
        else:  # - raz listes des talents, elements et races si sauvegarde ok -
            self.state_bar.update_vltexte(f" Info : Carte {typecard} '{name}' sauvegardée avec succès")
            self.__clear_multisetlist()
    
    def __save_terrain(self) -> str:
        # ------------------- création de l'objet 'terrain' ------------------
        terrain_card = Terrain(name=self.vname.get(),
                               cost=self.vcost.get(),
                               currency=self.vcurencytype.get(),
                               effects=self.get_effets()
                               )
        return writeFile(terrain_card, overwrite=True)
                        
    def __save_spell(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        spell_card = Spell(name=self.vname.get(),
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
                           talent=self.get_talents(),
                           elementType=self.get_elements()
                           )
        return writeFile(spell_card,overwrite=True)
                    
    def __save_equipement(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        equipement_card = Equipment(weaponType=self.varmesequip.get(),
                                    elementType=self.get_elements(),
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
                                    talent=self.get_talents(),
                                    race=self.get_races()
                                    )
        return writeFile(equipement_card,overwrite=True)
    
    def __save_creature(self) -> str:
        # ------------------- création de l'objet 'Creature' ------------------
        creature_card = Creature(race=self.vraces.get(),
                                 elementType=self.get_elements(),
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
                                 talent=self.get_talents()                                 
                                 )
        return writeFile(creature_card,overwrite=True)



    def fenetre_a_propos(self, event:tk.Event=None):
        """ Fenêtre-message à propos.
            Indique le nom du/des auteurs ainsi que la/les licences.
        """
        message = "CARDDB GUI v1.0"+"\n\nCopyright (C) 2026\nBernard Amouroux" \
        "\nLicense : GPL Version 3, 29 June 2007\n" \
        "\nMoteur du support de création des cartes"+"\nJan Amouroux" \
        "\nMIT License (c) 2026 Jan Amouroux\n" \
        "\nSur une Idée originale de Messieurs\n Doricam l'Argentin et LeCurieux\n"
        self.MessageBox.textfont('Times 15 normal roman')
        self.MessageBox.boxtitle('À propos')
        self.MessageBox.message = message
    
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
    app.title("CARDDB GUI v1.0 (c)2025 AMOUROUX Bernard - GUI de saisie des cartes de CARDDB (c)2026 AMOUROUX Jan")
    app.mainloop()
        