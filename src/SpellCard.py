
from Card import Card
from CombatData import CombatData
import cardLogics


class Spell(Card):
    def __init__(self, name: str, cost: int, currency: str, cardImg:str,
                typeSort:str,
                hp:int=0, crit:int=0 ,atk:int=0,  defense:int=0, heal:int=0, target:str|None=None,
                race:str|None=None, weaponType:str|None=None,
                talent: str | None = None, elementType: tuple[str,...] | str |None = None) -> None:
        
        if typeSort.lower() not in cardLogics.readRules("sort"):
            raise ValueError("type de sort innexistant")
        
        if race not in cardLogics.readRules("races") and not race == None:
            raise ValueError("race innexistante")
        
        if weaponType not in cardLogics.readRules("armes") and not weaponType == None:
            raise ValueError("type d'arme erreur")
        
        self.elementType = cardLogics.elementTest(elementType)
            
        super().__init__(name=name, cost=cost, 
                        currency=currency, talent=talent, 
                        elementType=elementType, cardImg=cardImg)

        self.combatStat = CombatData(hp, crit, atk, defense, heal, target)
        if isinstance(race,str) : race.lower()
        self.race = race
        self.weaponType=weaponType
        self.typeSort = typeSort.lower()
        self.cardType = "spell"

    def __eq__(self, value: object) -> bool:
        """__equals__

        Args:
            value (object): une autre Creature

        Returns:
            bool: true si les 2 cartes ont les mêmes valeurs sur toutes les variables
        """
        if not isinstance(value, Spell):
            return False
        outTrueFalse = []
        outTrueFalse.append(super().__eq__(value))
        outTrueFalse.append(self.combatStat == value.combatStat)
        outTrueFalse.append(self.weaponType == value.weaponType)
        outTrueFalse.append(self.race == value.race)
        outTrueFalse.append(self.typeSort == value.typeSort)

        return all(outTrueFalse)