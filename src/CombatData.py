from dataclasses import dataclass

@dataclass
class CombatData:
    def __init__(self, hp:int, crit:int ,atk:int=0,  defense:int=0, heal:int=0, target:str|None=None) -> None:
        """
        détermine les attributs de combat d'une carte, l'atk et la defense sur les équipements représentent les bonus de l'équipement à son porteur

        Args:
            hp (int): Heal Points, soit les points de vie de la carte
            crit (int): la valeur de critique, soit le dé qui doit être réussi afin d'effectuer le crit
            atk (int, optional): valeur d'attaque de la carte. Defaults to 0.
            defense (int, optional): valeur de defense de la carte. Defaults to 0.
            heal (int, optional): Si >0, la carte peut soigner, dans ce cas de combien. Defaults to 0.
            target (str | None, optional): le type de ciblage de la carte, si un équipement en donne un remplace le ciblage de la créature qui l'équipe. Defaults to None.

        Raises:
            ValueError: si pv|atk|def<0 ou si le crit ne correspond pas a un dé ou si le ciblage n'existe pas
        """
        if target : target = target.lower()
        if hp<0 :
            raise ValueError("valeur PV impossible")
        if atk<0 :
            raise ValueError("valeur atk impossible")
        if defense < 0 :
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
        self.defense = defense
        self.heal = heal
        self.target = target
        
    def __eq__(self, value: object) -> bool:
        """__equals__

        Args:
            value (object): une autre CombatData

        Returns:
            bool: true si les 2 cartes ont les mêmes valeurs sur toutes les variables
        """
        if not isinstance(value, CombatData):
            return False
        
        outTrueFalse = []
        outTrueFalse.append(self.hp == value.hp)
        outTrueFalse.append(self.crit == value.crit)
        outTrueFalse.append(self.atk == value.atk)
        outTrueFalse.append(self.defense == value.defense)
        outTrueFalse.append(self.heal == value.heal)
        outTrueFalse.append(self.target == value.target)
        
        return all(outTrueFalse)
    
    def __str__(self) -> str:
        return f"hp: {self.hp}, crit: {self.crit}"