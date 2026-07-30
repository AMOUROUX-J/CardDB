from Card import Card
from CombatData import CombatData
from dataclasses import dataclass

@dataclass
class Equipment(Card):
    def __init__(self, weaponType:str|None ,elementType:list[str], itemType:str,
                name: str, cost: int, currency: str,
                hp:int=0, crit:int=0 ,atk:int=0,  defence:int=0, heal:int=0, target:str|None=None, talent: list[str]|None=None, race:list[str]=[]# pyright: ignore[reportArgumentType]
                ) -> None:
        
        super().__init__(name, cost, currency, talent, elementType) # pyright: ignore[reportArgumentType]
        self.combatStat = CombatData(hp, crit, atk, defence, heal, target)
        self.type = itemType
        self.weaponType = weaponType
        self.race = race