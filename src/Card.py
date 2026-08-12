
from dataclasses import dataclass
import os.path as osp
import cardLogics

@dataclass
class Card:
    
    CardDBOutPath:str = osp.join("./","cardsData")
    ImageOutPath:str = osp.join("./","imgsDataDB","cardImages")
    
    def __init__(self, name: str, cost: int, currency: str, talent: str|None, elementType:tuple[str,...]|str|None, effects:list[str|None]|str|None=None, cardImg:str=f"{ImageOutPath}/placeholder.png") -> None:
        """
        crée la carte

        Args:
            name (str): nom de la carte
            cost (int): prix
            currency (str): type de monnaie nécessaire
            talent (list[str] | str | None): si a des talents
            elementType (list[str]): liste des éléments de la carte

        Raises:
            ValueError: si la monnaie de la carte n'est pas les les règles de types de monnaie
            ValueError: si la carte coute moins que 0
        """
        
        if not name :
            raise ValueError("le nom d'une carte 'CardDB' doit être renseigné avec au moins 1 caractères")
        
        if currency not in cardLogics.readRules("monnaie"):
            raise ValueError("type de monnaie inexistante")
        
        if cost <0 :
            raise ValueError("le prix doit être supérieur à 0")
        
        if not isinstance(effects, list): 
            effects = [effects,]
        
        # nom absolu du fichier Image de la carte
        self.imageFilename = cardImg
        # ----------- récupération de l'extension du fichier image ------------
        fname, ext = osp.splitext(cardImg)
        # -------- Nom de l'image et chemin ou elle doit être copiées ---------
        self.outPath = osp.join("./",Card.ImageOutPath,f"CardType_{name.replace(" ","_")}{ext}")
        
        self.name = name.replace(" ","_")
        self.cost = cost
        self.currency = currency
        self.talent = talent
        self.effects = effects
        self.elementType = cardLogics.elementTest(elementType)
        
    def __str__(self) -> str:
        return f"{self.name}, coût: {self.cost}, type de monnaie: {self.currency}, talent: {self.talent}, éléments: {self.elementType}"    
    
    def __eq__(self, value: object) -> bool:
        """__equals__

        Args:
            value (object): une autre carte

        Returns:
            bool: true si les 2 cartes ont les mêmes valeurs sur toutes les variables
        """
        if not isinstance(value, Card):
            return False
        
        outTrueFalse = []
        outTrueFalse.append(self.name == value.name)
        outTrueFalse.append(self.cost == value.cost)
        outTrueFalse.append(self.talent == value.talent)
        outTrueFalse.append(self.currency == value.currency)
        outTrueFalse.append(self.elementType == value.elementType)
        
        return all(outTrueFalse)




if __name__ == "__main__":
    
    card = Card("test1",2,"bleu",None,None)
    [print(f"{key:<17}: {getattr(card, key)}") for key in card.__dict__.keys()]