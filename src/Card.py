from dataclasses import dataclass
from types import NoneType
import cardLogics

@dataclass
class Card:
    
    def __init__(self, name: str, cost: int, currency: str, talent: list[str]|str|None, elementType:list[str|None]|str|None) -> None:
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
        if not isinstance(elementType,list):
            self.elementType = [].append(elementType)
        else:
            self.elementType = elementType
    
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
        
        #return not False in outTrueFalse
        return all(outTrueFalse)

    """
    not False in outTrueFalse vérifie seulement qu’il n’y a pas de False dans la liste.

    Ça revient à not (False in outTrueFalse).
    Mais False in [0] est True en Python, donc cette expression peut donner un résultat surprenant si ta liste contient des valeurs équivalentes à False comme 0.
    all(x == True for x in outTrueFalse) vérifie que chaque élément est égal à True.

    C’est plus explicite.
    Mais 1 == True est aussi True, donc ce n’est pas strictement “vrai booléen”.
    
    Le plus robuste / pythonique
    Si tu veux simplement savoir si tous les éléments sont évalués comme vrais :
        return all(outTrueFalse)
    Si tu veux vérifier que tous les éléments sont exactement True :
        return all(x is True for x in outTrueFalse)

    Conclusion
    Meilleur choix si tu veux robustesse et clarté : all(outTrueFalse)
    Si tu veux booleans exacts : all(x is True for x in outTrueFalse)
    """
    
