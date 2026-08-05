from Card import Card
from CombatData import CombatData
from dataclasses import dataclass

import cardLogics

@dataclass
class Equipment(Card):
    def __init__(self, weaponType:str|None ,elementType:list[str], itemType:str,
                name: str, cost: int, currency: str,
                hp:int=0, crit:int=0 ,atk:int=0,  defense:int=0, heal:int=0, target:str|None=None, talent: list[str]|None=None, race:list[str]=[]# pyright: ignore[reportArgumentType]
                ) -> None:
        """
        crée l'équipement (armure ou arme)

        Args:
            weaponType (str | None): le type d'arme (distance, deux main, ...)
            elementType (list[str]): elements fournis par l'arme
            itemType (str): si arme ou armure
            name (str): nom
            cost (int): coût
            currency (str): type de monnaie
            hp (int, optional): valeur de pv. Defaults to 0.
            crit (int, optional): valeur de crit . Defaults to 0.
            atk (int, optional): valeur d'atk. Defaults to 0.
            defense (int, optional): valeur de defense. Defaults to 0.
            heal (int, optional): valeur de soin. Defaults to 0.
            target (str | None, optional): type de ciblage. Defaults to None.
            talent (list[str] | None, optional): si a telents les listes. Defaults to None.
            race (list[str], optional): quelle race peut s'équiper de cette arme. Defaults to [].
            
        Raises:
            ValueError: si race|arme|elements absent des règles
        """
        if isinstance(race, list) and race:
            race = [i.lower() for i in race]
            for i in race:
                if i not in cardLogics.readRules("races"):
                    raise ValueError("race inexistante")
        else :
            if race not in cardLogics.readRules("races") and not race == []:
                raise ValueError("race inexistante")
            
        if weaponType not in cardLogics.readRules("armes") and not weaponType == None:
            raise ValueError("type d'arme erreur")
        
        
        for currentType in elementType:
            if currentType not in cardLogics.readRules("elements") and not currentType == None:
                raise ValueError("element invalide")

        super().__init__(name, cost, currency, talent, elementType) # pyright: ignore[reportArgumentType]
        self.combatStat = CombatData(hp, crit, atk, defense, heal, target)
        self.cardType = "equipement"
        self.equipmentType = itemType
        self.weaponType = weaponType
        self.race = race
        
        def __str__(self) -> str:
            return f"{self.cardType}, {self.name}"
    
    def __eq__(self, value: object) -> bool:
        """__equals__
        Args:
            value (object): une autre Creature

        Returns:
            bool: true si les 2 cartes ont les mêmes valeurs sur toutes les variables
        """
        if not isinstance(value, Equipment):
            return False
        outTrueFalse = []
        outTrueFalse.append(super().__eq__(value))
        outTrueFalse.append(self.combatStat == value.combatStat)
        outTrueFalse.append(self.weaponType == value.weaponType)
        outTrueFalse.append(self.race == value.race)
        outTrueFalse.append(self.equipmentType == value.equipmentType)

        return all(outTrueFalse)