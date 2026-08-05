
from Card import Card
from CombatData import CombatData
import cardLogics


class Spell(Card):
    def __init__(self, name: str, cost: int, currency: str,
                typeSort:str,
                hp:int=0, crit:int=0 ,atk:int=0,  defense:int=0, heal:int=0, target:str|None=None,
                race:str|None=None, weaponType:str|None=None,
                talent: list[str] | str | None=None, elementType: list[str|None]=[None]) -> None:
        
        if typeSort.lower() not in cardLogics.readRules("sort"):
            raise ValueError("type de sort innexistant")
        
        if race not in cardLogics.readRules("races") and not race == None:
            raise ValueError("race innexistante")
        
        if weaponType not in cardLogics.readRules("armes") and not weaponType == None:
            raise ValueError("type d'arme erreur")
        
        for currentType in elementType:
            if currentType not in cardLogics.readRules("elements"):
                raise ValueError("element invalide")
            
        super().__init__(name, cost, currency, talent, elementType)

        self.combatStat = CombatData(hp, crit, atk, defense, heal, target)
        if isinstance(race,str) : race.lower()
        self.race = race
        self.weaponType=weaponType
        self.typeSort = typeSort.lower()
        self.cardType = "spell"
