
def readRules(whichRule:str) -> list[str]:
    """
    Va chercher les règles du dossier ./coreDataDB (permet d'éviter les erreurs de BD)

    Args:
        whichRule (str): quel fichier règle lire

    Returns:
        list[str]: la liste des catégories existantes
    """
    
    fooPath= fr"./coreDataDB/{whichRule}"
    with open(file=fooPath,encoding='utf8',mode='r') as inFile:
            outRules = [i.strip() for i in inFile.readlines()]
    return outRules