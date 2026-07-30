from pathlib import Path
import Card
from equipmentCard import Equipment
from CreatureCard import Creature
import json

def createCard(Cardtype:str):
    pass

def readFile(name:str,cardType:str):
    pathToFile = f"./cardsData/{cardType}_{name}.json"
    with open(file=pathToFile,encoding='utf8',mode='r') as inFile:
        data = json.load(inFile)
    
    match cardType :
        case "creature":
            return Creature(name=data["name"],
                            hp= data["hp"],
                            atk=data["atk"],
                            defence=data["def"],
                            heal=data["heal"],
                            currency=data["costType"],
                            cost=data["cost"],
                            talent=data["talent"],
                            elementType=[data["type1"],data['type2']],
                            crit=data["crit"],
                            race=data["race"],
                            weaponType=data["weapon"],
                            target=data["targeting"]
                            )
        
        case "equipment":
            return Equipment(
                    name=data["name"],
                    hp= data["hp"],
                    atk=data["atk"],
                    defence=data["def"],
                    heal=data["heal"],
                    currency=data["costType"],
                    cost=data["cost"],
                    talent=data["talent"],
                    elementType=[data["type1"],data['type2']],
                    crit=data["crit"],
                    race=data["race"],
                    weaponType=data["weapon"],
                    target=data["targeting"],
                    itemType=data["itemType"],
            )

def writeFile(card, overwrite: bool = False):
    name = card.name
    cardType = card.cardtype

    pathToFile = f"./cardsData/{cardType}_{name}.json"
    p = Path(pathToFile)
    if p.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {pathToFile}. Pass overwrite=True to replace it.")
    
    payload = {
        "name": card.name,
        "hp": card.combatStat.hp,
        "atk": card.combatStat.atk,
        "def": card.combatStat.defence,
        "heal": card.combatStat.heal,
        "costType": card.currency,
        "cost": card.cost,
        "talent": card.talent,
        "type1": card.elementType[0] if len(card.elementType) > 0 else None,
        "type2": card.elementType[1] if len(card.elementType) > 1 else None,
        "crit": card.combatStat.crit,
        "race": getattr(card, "race", None),
        "weapon": getattr(card, "weaponType", None),
        "targeting": card.combatStat.target,
    }

    # if isinstance(card, Equipment):
    #     payload["itemType"] = getattr(card, "type", None)

    with open(file= pathToFile, mode="w", encoding='utf8') as outFile:
        json.dump(payload, outFile, ensure_ascii=False, indent=2)
        
    print(f"done at {pathToFile}")

    return pathToFile


if __name__ == "__main__":
    eweCard = Creature(race="magique",weaponType="lourd",elementType=["special"],name="ewe",cost=5,talent="increvable",currency="money",hp=15,crit=8,atk=10,defence=0,heal=3,target="mono")
    writeFile(eweCard,overwrite=True)
    readFile("ewe","creature")
