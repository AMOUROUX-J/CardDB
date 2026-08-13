from os import path
from Card import Card


class Terrain(Card):
    def __init__(self, name: str, effects: list[str]|str, cardImg:str=f"{Card.ImageOutPath}/placeholder.png") -> None:
        r""" Crée une carte CardDB de type 'terrain'
        Args:
            name (str): nom du terrain
            effets (list[str]): liste des effets actifs sur le terrain
            cardImg (str): le chemin de l'image (sera copier dans : imgsDataDB\cardImages\)
            effects (list[str] | str): liste des effects du terrain sur la partie
        """
        super().__init__(name, cost=0, currency="money", talent=None, elementType=None, effects=effects, cardImg=cardImg) # pyright: ignore[reportArgumentType]
        
        if not isinstance(effects,list):
            effects = [effects,]
        self.name = name
        self.effects = effects
        self.cardType = "terrain"
        # nom absolu du fichier de l'image de la carte
        self.imageFilename = cardImg    
        
    def __eq__(self, value: object) -> bool:
        """__equals__
        Args:
            value (object): une autre Terrain
        Returns:
            bool: true si les 2 cartes ont les mêmes valeurs sur toutes les variables
        """
        if not isinstance(value, Terrain):
            return False

        outTrueFalse = []
        outTrueFalse.append(self.name == value.name)
        outTrueFalse.append(self.effects == value.effects)
        outTrueFalse.append(self.imageFilename == value.imageFilename)
        
        return all(outTrueFalse)