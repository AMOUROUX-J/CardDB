from dataclasses import dataclass
from Card import Card
from CombatData import CombatData
import cardLogics

@dataclass
class Creature(Card):
    def __init__(self,
                race:str, 
                elementType:list[str],
                name: str, 
                cost: int, 
                currency: str,
                hp:int, crit:int=0 ,atk:int=0,  defense:int=0, heal:int=0, target:str="mono",weaponType:str=None, talent: str=None # pyright: ignore[reportArgumentType]
                ) -> None:
        """
        crée la créature

        Args:
            race (str): race de la carte
            elementType (list[str]): liste des éléments
            name (str): nom
            cost (int): coût
            currency (str): type de monnaie
            hp (int, optional): valeur de pv.
            crit (int, optional): valeur de crit. Defaults to 0.
            atk (int, optional): valeur d'attaque. Defaults to 0.
            defence (int, optional): valeur de défense. Defaults to 0.
            heal (int, optional): valeur de soin. Defaults to 0.
            target (str, optional): type de ciblage. Defaults to "mono".
            weaponType (str, optional): type d'arme équipable. Defaults to None.
            talent (_type_, optional): si à talent ses talents. Defaults to None.

        Raises:
            ValueError: si race absent des règles
            ValueError: si arme absent des règles
            ValueError: si elements absent des règles
        """
        
        if race not in cardLogics.readRules("races"):
            raise ValueError("race innexistante")
        
        if weaponType not in cardLogics.readRules("armes") and not weaponType == None:
            raise ValueError("type d'arme erreur")
        
        for currentType in elementType:
            if currentType not in cardLogics.readRules("elements"):
                raise ValueError("element invalide")
        
        super().__init__(name, cost, currency, talent, elementType) # pyright: ignore[reportArgumentType]
        self.combatStat = CombatData(hp, crit, atk, defense, heal, target)
        self.weaponType= weaponType
        self.cardType = "creature"
        self.race = race.lower()