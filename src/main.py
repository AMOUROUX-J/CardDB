from pathlib import Path
import cardLogics
from equipmentCard import Equipment
from CreatureCard import Creature
import json

def getKeybordData() -> dict[str, str]:
    """
    Méthode temp pour crée les cartes. itemType ne sert que pour des équipements

    Returns:
        dict[str, str]: les données complete de la carte à crée
    """
    
    outData = {
        "name":input("name: "),
        "hp": input("hp: "),
        "atk":input("atk: "),
        "defence":input("def: "),
        "heal":input("heal: "),
        "currency":input("costType: "),
        "cost":input("cost: "),
        "talent":input("talent: "),
        'type1':input("type2: "),
        'type2':('type2: '),
        "crit":input("crit: "),
        "race":input("race: "),
        "weaponType":input("weapon: "),
        "target":input("targeting: "),
        "itemType":input("itemType")
    }
    return outData

def createCard(Cardtype:str, data:dict={}) -> Creature | Equipment | None:
    """
    Génère un objet Card soit depuis un dico contenant un dico des donnés si aucun dico fourni, demande toutes les données via des input() (temp en attendant l'IG)

    Args:
        Cardtype (str): type de carte, pour l'instant reçois : creature ou equipment
        data (dict, optional): le dictionnaire des données. Defaults to {}.

    Raises:
        ValueError: si le type de carte n'existe pas dans la BD
    
    Returns:
        Card: un objet Card
    """
    
    if not data:
        data = getKeybordData()
    
    match Cardtype :
            case "creature":
                return Creature(name=data["name"],
                            hp= data["hp"],
                            atk=data["atk"],
                            defense=data["def"],
                            heal=data["heal"],
                            currency=data["costType"],
                            cost=data["cost"],
                            talent=data["talent"],
                            elementType=data["types"],
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
            case _:
                raise ValueError("type de carte non supporté")

def readFile(name:str,cardType:str) -> Creature | Equipment | None:
    """
    extrait les données d'une carte à partir des fichiers. chaque carte a son nom sous forme `{type de carte}_{nom carte}`

    Args:
        name (str): nom de la carte
        cardType (str): ty de carte

    Returns:
        Card: renvoie la carte
    """
    
    pathToFile = f"./cardsData/{cardType}_{name}.json"
    with open(file=pathToFile,encoding='utf8',mode='r') as inFile:
        data = json.load(inFile)
    
    match cardType :
        case "creature":
            return createCard("creature",data)
        
        case "equipment":
            return createCard("equipment",data)

def writeFile(card, overwrite: bool = False) -> str:
    """
    Enregistre la carte dans le dossier ./cardsData avec le nom sous format `{type de carte}_{nom carte}`

    Args:
        card (Card): l'objet Card
        overwrite (bool, optional): si oui ou non écrase si la carte existe déjà. Defaults to False.

    Raises:
        FileExistsError: si overwrite == False empêche d'écraser la carte déjà existante

    Returns:
        str: le chemin ou la carte à été enregistrer
    """
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
        "types": card.elementType if len(card.elementType) > 0 else None,
        "crit": card.combatStat.crit,
        "race": getattr(card, "race", None),
        "weapon": getattr(card, "weaponType", None),
        "targeting": card.combatStat.target,
    }

    with open(file= pathToFile, mode="w", encoding='utf8') as outFile:
        json.dump(payload, outFile, ensure_ascii=False, indent=2)
    print(f"done at {pathToFile}")

    return pathToFile

if __name__ == "__main__":
    eweCard = Creature(race="magique",weaponType="lourd",elementType=["special"],name="ewe",cost=5,talent="increvable",currency="money",hp=15,crit=8,atk=10,defense=0,heal=3,target="mono")
    writeFile(eweCard,overwrite=True)
    creature = readFile("ewe","creature")
    #[print(f"\t{key:15}: {getattr(creature, key)}") for key in creature.__dict__.keys()]
