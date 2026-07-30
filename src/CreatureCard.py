from dataclasses import dataclass
from Card import Card
from CombatData import CombatData

@dataclass
class Creature(Card):
    def __init__(self,
                race:str, elementType:list[str],
                name: str, cost: int, currency: str,
                hp:int=0, crit:int=0 ,atk:int=0,  defence:int=0, heal:int=0, target:str="mono",weaponType:str=None, talent: str=None # pyright: ignore[reportArgumentType]
                ) -> None:
        
        if race not in ["magique","vegetal","artificiel","humanoide","animal"]:
            raise ValueError("race innexistante")
        
        if weaponType not in ["distance","lourd","leger","toutes",None]:
            raise ValueError("type d'arme erreur")
        
        for currentType in elementType:
            if currentType not in ["feu","eau","terre","plante","magie","lumiere","tenebre","special","electrique","dryade","acier",None]:
                raise ValueError("element invalide")
        
        super().__init__(name, cost, currency, talent, elementType)
        self.combatStat = CombatData(hp, crit, atk, defence, heal, target)
        self.weaponType= weaponType
        self.cardtype = "creature"
        self.race = race