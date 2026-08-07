from os import name
from pathlib import Path
from SpellCard import Spell
from equipmentCard import Equipment
from CreatureCard import Creature
import json

from test_card import Terrain

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
        'types':input("types: "),
        "crit":input("crit: "),
        "race":input("race: "),
        "weaponType":input("weapon: "),
        "target":input("targeting: "),
        "itemType":input("itemType")
    }
    return outData

def createCard(Cardtype:str, data:dict={}) -> Creature | Equipment | Spell | Terrain:
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
                            currency=data["currency"],
                            cost=data["cost"],
                            talent=data["talent"],
                            elementType=data["types"],
                            crit=data["crit"],
                            race=data["race"],
                            weaponType=data["weapon"],
                            target=data["targeting"]
                            )
                
            case "equipement":
                return Equipment(
                    name=data["name"],
                    hp= data["hp"],
                    atk=data["atk"],
                    defense=data["def"],
                    heal=data["heal"],
                    currency=data["currency"],
                    cost=data["cost"],
                    talent=data["talent"],
                    elementType=data["types"],
                    crit=data["crit"],
                    race=data["race"],
                    target=data["targeting"],
                    weaponType=data["weapon"],
                    itemType=data["itemType"]
            )
            case "spell":
                return Spell(
                    name=data["name"],
                    hp= data["hp"],
                    atk=data["atk"],
                    defense=data["def"],
                    heal=data["heal"],
                    currency=data["currency"],
                    cost=data["cost"],
                    talent=data["talent"],
                    elementType=data["types"],
                    crit=data["crit"],
                    race=data["race"],
                    weaponType=data["weapon"],
                    target=data["targeting"],
                    typeSort=data["typeSort"]
                )
            case "terrain":
                return Terrain(
                    name=data["name"],
                    cost=data["cost"],
                    currency=data["currency"],
                    effects=data["effects"]
                )
            case _:
                raise ValueError("type de carte non supporté")

def readFile(name:str,cardType:str) -> Creature | Equipment | Spell | Terrain:
    """
    extrait les données d'une carte à partir des fichiers. chaque carte a son nom sous forme `{type de carte}_{nom carte}`

    Args:
        name (str): nom de la carte
        cardType (str): type de la carte

    Returns:
        Card: renvoie la carte
    """
    
    pathToFile = f"./cardsData/{cardType}_{name}.json"
    with open(file=pathToFile,encoding='utf8',mode='r') as inFile:
        data = json.load(inFile)
    
    match cardType :
        case "creature":
            return createCard("creature",data)
        
        case 'equipement':
            return createCard("equipement",data)
        
        case "spell":
            return createCard("spell",data)

        case "terrain":
            return createCard("terrain",data)
        
        case _:
            raise ValueError("type de carte inexistante")

def writeFile(card:Equipment | Creature | Spell | Terrain, overwrite: bool = False) -> str:
    """
    Enregistre la carte dans le dossier ./cardsData avec le nom sous format `{type de carte}_{nom carte}`

    Args:
        card (Card): l'objet Card
        overwrite (bool, optional): si oui ou non écrase si la carte existe déjà. Defaults to False.

    Raises:
        FileExistsError: si overwrite == False empêche d'écraser la carte déjà existante

    Returns:
        str: le chemin ou la carte à été enregistrée
    """
    name = card.name
    cardType = card.cardType

    pathToFile = f"./cardsData/{cardType}_{name}.json"
    p = Path(pathToFile)
    if p.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {pathToFile}. Pass overwrite=True to replace it.")
    
    # les terrains son spéciaux et sont traité a-part
    if isinstance(card,Terrain):
        payload = {
            "name": card.name,
            "cost": card.cost,
            "currency": card.currency,
            "cardType": card.cardType,
            "effects": card.effects
        }
    
    else :
        payload = {
            "name": card.name,
            "hp": card.combatStat.hp,
            "atk": card.combatStat.atk,
            "def": card.combatStat.defense,
            "heal": card.combatStat.heal,
            "currency": card.currency,
            "cost": card.cost,
            "talent": getattr(card, 'talent', None),
            "types": getattr(card, "elementType", None),
            "crit": card.combatStat.crit,
            "race": getattr(card, "race", None),
            "weapon": getattr(card, "weaponType", None),
            "targeting": card.combatStat.target,
            "cardType": card.cardType
        }
        if isinstance(card,Equipment):
            payload["weaponType"]= card.weaponType
            payload["itemType"]=card.equipmentType # pyright: ignore[reportAttributeAccessIssue]

        if isinstance(card,Spell):
            payload["typeSort"]=card.typeSort # pyright: ignore[reportAttributeAccessIssue]

    with open(file= pathToFile, mode="w", encoding='utf8') as outFile:
        json.dump(payload, outFile, ensure_ascii=False, indent=2)

    return pathToFile
