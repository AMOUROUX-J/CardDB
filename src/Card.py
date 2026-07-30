from dataclasses import dataclass
import cardLogics

@dataclass
class Card:
    
    def __init__(self, name: str, cost: int, currency: str, talent: list[str]|str|None, elementType:list[str|None]) -> None:
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
        
        if currency not in cardLogics.readRules("monnaie"):
            raise ValueError("type de monnaie inexistante")
        
        if cost <0 :
            raise ValueError("le prix doit être supérieur à 0")
        
        self.name = name
        self.cost = cost
        self.currency = currency
        if not isinstance(talent,list):
            self.talent = [talent]
        else:
            self.talent = talent
        self.elementType = list(elementType)
    
    
