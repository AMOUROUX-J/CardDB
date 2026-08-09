from dataclasses import dataclass
import cardLogics
import shutil

@dataclass
class Card:
    
    def __init__(self, name: str, cost: int, currency: str, talent: str|None, elementType:tuple[str,...]|str|None, cardImg:str="imgsDataDB/cardImages/placeHolder.jpg") -> None:
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
        
        if not name or len(name) <4 :
            raise ValueError("le nom d'une carte 'CardDB' doit être renseigné avec au moins 4 caractères")
        
        if currency not in cardLogics.readRules("monnaie"):
            raise ValueError("type de monnaie inexistante")
        
        if cost <0 :
            raise ValueError("le prix doit être supérieur à 0")
        
        # chemin ou les cartes vont être copiées
        self.outPath = f"imgsDataDB/cardImages/{name}"
        # nom du fichier Image de la carte
        self.imageFilename:str = ""
         
        self.name = name
        self.cost = cost
        self.currency = currency
        self.talent = talent
        self.elementType = cardLogics.elementTest(elementType)
    
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

