from dataclasses import dataclass

@dataclass
class CombatData:
    def __init__(self, hp:int, crit:int ,atk:int=0,  defence:int=0, heal:int=0, target:str|None=None) -> None:
        if hp<0 :
            raise ValueError("valeur PV impossible")
        if atk<0 :
            raise ValueError("valeur atk impossible")
        if defence < 0 :
            raise ValueError("valeur defence impossible")
        if heal<0 :
            raise ValueError("valeur heal impossible")
        if crit not in [0,2,6,8,20]:
            raise ValueError("valeur crit impossible")
        if target not in ["mono","zone","groupe",None]:
            raise ValueError("ciblage impossible")
        
        
        self.hp = hp
        self.crit = crit
        self.atk = atk
        self.defence = defence
        self.heal = heal
        self.target = target