
from Card import Card


class Terrain(Card):
    def __init__(self, name: str, cost: int, currency: str, effects: list[str]|str) -> None:
        """crée un terrain

        Args:
            name (str): nom du terrain
            cost (int): coût
            currency (str): type de coût
            effects (list[str] | str): liste des effects du terrain sur la partie
        """
        super().__init__(name, cost, currency, talent=None, elementType= None)
        if not isinstance(effects,list):
            effects = [effects,]
        self.cardType = "terrain"
        self.effects = effects
    
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
        outTrueFalse.append(self.cost == value.cost)
        outTrueFalse.append(self.currency == value.currency)
        outTrueFalse.append(self.effects == value.effects)
        
        return all(outTrueFalse)