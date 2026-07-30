import unittest
import cardLogics
from equipmentCard import Equipment
from CreatureCard import Creature
from SpellCard import Spell

class TestCard(unittest.TestCase):
    
    def testCreatureCardCreate(self) -> None:
        eweCard = Creature(race="magique",weaponType="lourd",elementType=["special"],name="ewe",cost=5,talent="increvable",currency="money",hp=15,crit=8,atk=10,defense=0,heal=3,target="mono")
        self.assertEqual(eweCard.name,"ewe")
        self.assertEqual(eweCard.combatStat.hp ,15)
        self.assertEqual(eweCard.combatStat.atk ,10)
        self.assertEqual(eweCard.combatStat.defence ,0)
        self.assertEqual(eweCard.combatStat.heal ,3)
        self.assertEqual(eweCard.combatStat.target ,"mono")
        self.assertEqual(eweCard.currency ,"money")
        self.assertEqual(eweCard.cost ,5)
        self.assertEqual(eweCard.talent ,["increvable"])
        self.assertEqual(eweCard.race ,"magique")
        self.assertEqual(eweCard.weaponType ,"lourd")
        self.assertEqual(eweCard.elementType ,["special"])
        self.assertEqual(eweCard.cardtype, "creature")

    def testCreatureMinInfo(self) -> None:
        smallCard = Creature(race="magique",elementType=["eau","special"],name="esprit de glace",cost=1,currency="bleu",atk=2,hp=5,crit=20)
        self.assertEqual(smallCard.name,"esprit de glace")
        self.assertEqual(smallCard.combatStat.hp ,5)
        self.assertEqual(smallCard.combatStat.atk ,2)
        self.assertEqual(smallCard.combatStat.defence ,0)
        self.assertEqual(smallCard.combatStat.heal ,0)
        self.assertEqual(smallCard.combatStat.target ,"mono")
        self.assertEqual(smallCard.currency ,"bleu")
        self.assertEqual(smallCard.cost ,1)
        self.assertEqual(smallCard.talent ,[None])
        self.assertEqual(smallCard.race ,"magique")
        self.assertEqual(smallCard.weaponType ,None)
        self.assertEqual(smallCard.elementType ,["eau","special"])
        self.assertEqual(smallCard.cardtype, "creature")

    def testWeaponCardCreate(self) -> None:
        armeCard = Equipment(itemType="arme",weaponType="lourd"  , elementType=[],name="pique Longue",cost=5,talent="Tueur d'animaux",currency="money",atk=3,defence=1) # pyright: ignore[reportArgumentType]
        self.assertEqual(armeCard.name,"pique Longue")
        self.assertEqual(armeCard.combatStat.hp ,0)
        self.assertEqual(armeCard.combatStat.atk ,3)
        self.assertEqual(armeCard.combatStat.defence ,1)
        self.assertEqual(armeCard.combatStat.heal ,0)
        self.assertEqual(armeCard.combatStat.target ,None)
        self.assertEqual(armeCard.currency ,"money")
        self.assertEqual(armeCard.cost ,5)
        self.assertEqual(armeCard.talent ,["Tueur d'animaux"])
        self.assertEqual(armeCard.race ,[])
        self.assertEqual(armeCard.weaponType ,"lourd")
        self.assertEqual(armeCard.elementType ,[])
        self.assertEqual(armeCard.type, "arme")

    def testArmorCardCreate(self) -> None:
        armorCard = Equipment(weaponType=None, itemType="armure", elementType=[], name="casque de combat", 
                        cost=3, currency="money", hp = 5, defence = 1, crit = 0, atk = 0, heal = 0,
                        target="mono",race=["magique","vegetal","artificiel","humanoide","animal"])
        self.assertEqual(armorCard.name,"casque de combat")
        self.assertEqual(armorCard.combatStat.hp ,5)
        self.assertEqual(armorCard.combatStat.atk ,0)
        self.assertEqual(armorCard.combatStat.defence ,1)
        self.assertEqual(armorCard.combatStat.heal ,0)
        self.assertEqual(armorCard.combatStat.target ,"mono")
        self.assertEqual(armorCard.currency ,"money")
        self.assertEqual(armorCard.cost ,3)
        self.assertEqual(armorCard.talent ,[None])
        self.assertEqual(armorCard.race ,["magique","vegetal","artificiel","humanoide","animal"])
        self.assertEqual(armorCard.weaponType ,None)
        self.assertEqual(armorCard.elementType ,[])
        self.assertEqual(armorCard.type, "armure")
    
    def testTankCardCreate(self) -> None: 
        tankCard = Equipment(elementType=["acier"], weaponType=None, itemType="armure", name="tank", cost=50, currency="money", hp=30, atk=15, defence=10, talent=["Absobtion","incurable"], race=["humanoide"])
        self.assertEqual(tankCard.name, "tank")
        self.assertEqual(tankCard.combatStat.hp, 30)
        self.assertEqual(tankCard.combatStat.atk, 15)
        self.assertEqual(tankCard.combatStat.defence, 10)
        self.assertEqual(tankCard.combatStat.heal, 0)
        self.assertEqual(tankCard.combatStat.target, None)
        self.assertEqual(tankCard.currency, "money")
        self.assertEqual(tankCard.cost, 50)
        self.assertEqual(tankCard.talent, ["Absobtion","incurable"])
        self.assertEqual(tankCard.race, ["humanoide"])
        self.assertEqual(tankCard.weaponType, None)
        self.assertEqual(tankCard.elementType, ["acier"])
        self.assertEqual(tankCard.type, "armure")

    def testreadRules(self) -> None:
        rulesList = cardLogics.readRules("testrule")
        self.assertIn("je",rulesList)
        self.assertIn("fonctionne",rulesList)
        self.assertIn("correctement Vraiment!!",rulesList)
        self.assertIn("1232CSF@:",rulesList)

    def testSpell1(self) -> None:
        spellCard = Spell(name="Assassinat",cost=9,currency="bleu",typeSort="actif",atk=10, elementType=["feu"], talent=["ne cible que les humanoïde"])
        self.assertEqual(spellCard.name, "Assassinat")
        self.assertEqual(spellCard.combatStat.hp, 0)
        self.assertEqual(spellCard.combatStat.atk, 10)
        self.assertEqual(spellCard.combatStat.defence, 0)
        self.assertEqual(spellCard.combatStat.heal, 0)
        self.assertEqual(spellCard.combatStat.target, None)
        self.assertEqual(spellCard.currency, "bleu")
        self.assertEqual(spellCard.cost, 9)
        self.assertEqual(spellCard.talent, ["ne cible que les humanoïde"])
        self.assertEqual(spellCard.race, None)
        self.assertEqual(spellCard.weaponType, None)
        self.assertEqual(spellCard.elementType, ["feu"])
        self.assertEqual(spellCard.typeSort, "actif")
        
    def testSpell2(self) -> None:
        spellCard = Spell(name="Cortilège de protection",cost=3,currency="bleu",typeSort="invocation",hp=10,defense=3,elementType=["feu"],race="artificiel",talent=["Muraille"])
        

if __name__ == "__main__":
    unittest.main(verbosity=2)
