from dataclasses import dataclass

@dataclass
class Card:
    
    def __init__(self, name: str, cost: int, currency: str, talent: list[str]|str|None, elementType:list[str]) -> None:
        
        if currency not in ["bleu", "rouge", "money"]:
            raise ValueError("type de monnaie inexistante")
        
        if cost <0 :
            raise ValueError("le prix doit être supérieur à 0")
        
        self.name = name
        self.cost = cost
        self.currency = currency
        self.talent = talent
        self.elementType = list(elementType)
    
    
    def readRules(self, whichRule:str):
        fileList = ["races","monaie","elements","armes"]
        if not whichRule in fileList:
            raise ValueError("")
        fooPath= fr"./coreDataDB\{whichRule}"
        with open(file=fooPath,encoding='utf8',mode='r') as inFile:
                list(",".join(inFile.readlines()))
        
