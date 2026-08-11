import unittest
import Card
import CombatData
from TerrainCard import Terrain
import cardLogics
from equipmentCard import Equipment
from CreatureCard import Creature
from SpellCard import Spell

import main

class TestCard(unittest.TestCase):
    
    def testCreatureCardCreate(self) -> None:
        eweCard = Creature(race="magique",weaponType="lourd",elementType="special",name="ewe",cost=5,talent="increvable",currency="money",hp=15,crit=8,atk=10,defense=0,heal=3,target="mono")
        self.assertEqual(eweCard.name,"ewe")
        self.assertEqual(eweCard.combatStat.hp ,15)
        self.assertEqual(eweCard.combatStat.atk ,10)
        self.assertEqual(eweCard.combatStat.defense ,0)
        self.assertEqual(eweCard.combatStat.heal ,3)
        self.assertEqual(eweCard.combatStat.target ,"mono")
        self.assertEqual(eweCard.currency ,"money")
        self.assertEqual(eweCard.cost ,5)
        self.assertEqual(eweCard.talent ,"increvable")
        self.assertEqual(eweCard.race ,"magique")
        self.assertEqual(eweCard.weaponType ,"lourd")
        self.assertEqual(eweCard.elementType ,("special",))
        self.assertEqual(eweCard.cardType, "creature")
        self.assertEqual(eweCard.effects, [None])


    def testCreatureMinInfo(self) -> None:
        smallCard = Creature(race="magique",elementType=("eau","special"),name="esprit de glace",cost=1,currency="bleu",atk=2,hp=5,crit=20)
        self.assertEqual(smallCard.name,"esprit_de_glace")
        self.assertEqual(smallCard.combatStat.hp ,5)
        self.assertEqual(smallCard.combatStat.atk ,2)
        self.assertEqual(smallCard.combatStat.defense ,0)
        self.assertEqual(smallCard.combatStat.heal ,0)
        self.assertEqual(smallCard.combatStat.target ,"mono")
        self.assertEqual(smallCard.currency ,"bleu")
        self.assertEqual(smallCard.cost ,1)
        self.assertEqual(smallCard.talent ,None)
        self.assertEqual(smallCard.race ,"magique")
        self.assertEqual(smallCard.weaponType ,None)
        self.assertEqual(smallCard.elementType ,("eau","special"))
        self.assertEqual(smallCard.cardType, "creature")
        self.assertEqual(smallCard.effects, [None])


    def testWeaponCardCreate(self) -> None:
        armeCard = Equipment(itemType="arme",weaponType="lourd"  , elementType=(),name="pique Longue",cost=5,talent="Tueur d'animaux",currency="money",atk=3,defense=1) # pyright: ignore[reportArgumentType]
        self.assertEqual(armeCard.name,"pique_Longue")
        self.assertEqual(armeCard.combatStat.hp ,0)
        self.assertEqual(armeCard.combatStat.atk ,3)
        self.assertEqual(armeCard.combatStat.defense ,1)
        self.assertEqual(armeCard.combatStat.heal ,0)
        self.assertEqual(armeCard.combatStat.target ,None)
        self.assertEqual(armeCard.currency ,"money")
        self.assertEqual(armeCard.cost ,5)
        self.assertEqual(armeCard.talent ,"Tueur d'animaux")
        self.assertEqual(armeCard.race ,[])
        self.assertEqual(armeCard.weaponType ,"lourd")
        self.assertEqual(armeCard.elementType ,None)
        self.assertEqual(armeCard.equipmentType, "arme")

    def testArmorCardCreate(self) -> None:
        armorCard = Equipment(weaponType=None, itemType="armure", elementType=None, name="casque de combat", 
                        cost=3, currency="money", hp = 5, defense = 1, crit = 0, atk = 0, heal = 0,
                        target="mono",race=["magique","vegetal","artificiel","humanoide","animal"])
        self.assertEqual(armorCard.name,"casque_de_combat")
        self.assertEqual(armorCard.combatStat.hp ,5)
        self.assertEqual(armorCard.combatStat.atk ,0)
        self.assertEqual(armorCard.combatStat.defense ,1)
        self.assertEqual(armorCard.combatStat.heal ,0)
        self.assertEqual(armorCard.combatStat.target ,"mono")
        self.assertEqual(armorCard.currency ,"money")
        self.assertEqual(armorCard.cost ,3)
        self.assertEqual(armorCard.talent ,None)
        self.assertEqual(armorCard.race ,["magique","vegetal","artificiel","humanoide","animal"])
        self.assertEqual(armorCard.weaponType ,None)
        self.assertEqual(armorCard.elementType ,None)
        self.assertEqual(armorCard.equipmentType, "armure")
        self.assertEqual(armorCard.effects, [None])
    
    def testTankCardCreate(self) -> None: 
        tankCard = Equipment(elementType="acier", weaponType=None, itemType="armure", name="tank", cost=50, currency="money", hp=30, atk=15, defense=10, talent="Absobtion", race=["humanoide"])
        self.assertEqual(tankCard.name, "tank")
        self.assertEqual(tankCard.combatStat.hp, 30)
        self.assertEqual(tankCard.combatStat.atk, 15)
        self.assertEqual(tankCard.combatStat.defense, 10)
        self.assertEqual(tankCard.combatStat.heal, 0)
        self.assertEqual(tankCard.combatStat.target, None)
        self.assertEqual(tankCard.currency, "money")
        self.assertEqual(tankCard.cost, 50)
        self.assertEqual(tankCard.talent, "Absobtion")
        self.assertEqual(tankCard.race, ["humanoide"])
        self.assertEqual(tankCard.weaponType, None)
        self.assertEqual(tankCard.elementType, ("acier",))
        self.assertEqual(tankCard.equipmentType, "armure")
        self.assertEqual(tankCard.effects, [None])


    def testreadRules(self) -> None:
        rulesList = cardLogics.readRules("testrule")
        self.assertIn("je",rulesList)
        self.assertIn("fonctionne",rulesList)
        self.assertIn("correctement Vraiment!!",rulesList)
        self.assertIn("1232CSF@:",rulesList)

    def testSpell1(self) -> None:
        spellCard = Spell(name="Assassinat",cost=9,currency="bleu",typeSort="actif",atk=10, elementType="feu", talent="Talent waouh")
        self.assertEqual(spellCard.name, "Assassinat")
        self.assertEqual(spellCard.combatStat.hp, 0)
        self.assertEqual(spellCard.combatStat.atk, 10)
        self.assertEqual(spellCard.combatStat.defense, 0)
        self.assertEqual(spellCard.combatStat.heal, 0)
        self.assertEqual(spellCard.combatStat.target, None)
        self.assertEqual(spellCard.currency, "bleu")
        self.assertEqual(spellCard.cost, 9)
        self.assertEqual(spellCard.talent, "Talent waouh")
        self.assertEqual(spellCard.race, None)
        self.assertEqual(spellCard.weaponType, None)
        self.assertEqual(spellCard.elementType, ("feu",))
        self.assertEqual(spellCard.typeSort, "actif")
        
    def testSpell2(self) -> None:
        spellCard = Spell(name="Cortilège de protection",cost=3,currency="bleu",typeSort="invocation",hp=10,defense=3,elementType="feu",race="artificiel",talent="Muraille", effects=["mange vos Ewes", "pile ou face"])
        self.assertEqual(spellCard.name, "Cortilège_de_protection")
        self.assertEqual(spellCard.combatStat.hp, 10)
        self.assertEqual(spellCard.combatStat.atk, 0)
        self.assertEqual(spellCard.combatStat.defense, 3)
        self.assertEqual(spellCard.combatStat.heal, 0)
        self.assertEqual(spellCard.combatStat.target, None)
        self.assertEqual(spellCard.currency, "bleu")
        self.assertEqual(spellCard.cost, 3)
        self.assertEqual(spellCard.talent, "Muraille")
        self.assertEqual(spellCard.race, "artificiel")
        self.assertEqual(spellCard.weaponType, None)
        self.assertEqual(spellCard.elementType, ("feu",))
        self.assertEqual(spellCard.typeSort, "invocation")
        self.assertEqual(spellCard.effects, ["mange vos Ewes", "pile ou face"])
        
    
    def testWriteReadEwe(self):
        eweCard = Creature(race="magique",weaponType="lourd",elementType="special",name="ewe",cost=5,talent="increvable",currency="money",hp=15,crit=8,atk=10,defense=0,heal=3,target="mono", effects=["vole vos sous", "Seconde chance", "créatrice de frac"])
        main.writeFile(eweCard, True)
        eweCopy = main.readFile("ewe","creature")
        self.assertEqual(eweCard,eweCopy)

    def testWriteReadCard(self) -> None:
        armeCard = Equipment(itemType="arme",weaponType="lourd", elementType=(),name="pique Longue",cost=5,talent="Tueur d'animaux",currency="money",atk=3,defense=1)
        main.writeFile(armeCard, overwrite=True)
        armeCardRead = main.readFile(armeCard.name, armeCard.cardType)
        self.assertTrue(armeCard.__eq__(armeCardRead))
        #[print(f"\n\t{key:15}: {getattr(armeCardRead, key)}") for key in armeCardRead.__dict__.keys()]
    
    def testWriteReadSpellCard(self) -> None:
        spellCard = Spell(name="Cortilège de protection",cost=3,currency="bleu",typeSort="invocation",hp=10,defense=3,elementType="feu",race="artificiel",talent="Muraille")
        main.writeFile(spellCard,True)
        spellread = main.readFile("Cortilège_de_protection", "spell")
        self.assertTrue(spellCard.__eq__(spellread))
    
    def test__eq__Card(self) -> None:
        card1 = Card.Card("test1",2,"bleu",None,None)
        card1bis = Card.Card("test1",5,"rouge",None,None)
        self.assertFalse(card1.__eq__(card1bis))
    
    def test__eq__CombatData(self) -> None:
        stat1 = CombatData.CombatData(hp=1,crit=2,atk=1,defense=1,heal=1,target=None)
        stat1Bis = CombatData.CombatData(hp=1,crit=2,atk=1,defense=1,heal=1,target=None)
        self.assertTrue(stat1 == stat1Bis)
    
    def test__eq__Creature(self) -> None:
        creature1 = Creature(race="humanoide",elementType="feu",name="testTest",cost=1,currency="bleu",hp=1)
        creature1bis = Creature(race="humanoide",elementType=("feu","eau"),name="testTest",cost=10,currency="bleu",hp=1)
        self.assertFalse(creature1 == creature1bis)
    
    def test__eq__Equipement(self) -> None:
        equipment1 = Equipment(weaponType="distance",itemType="distance",elementType="eau",name="testArme",cost=2,currency="rouge")
        equipment1bis = Equipment(weaponType="distance",itemType="distance",elementType="eau",name="testArme",cost=2,currency="rouge")
        self.assertTrue(equipment1 == equipment1bis)
    
    def testCreateTerrain(self) -> None:
        terrain = Terrain("test0",["sert de test","n'existe pas!!"])
        self.assertEqual(terrain.name, "test0")
        self.assertEqual(terrain.effects,["sert de test","n'existe pas!!"])
    
    def testWriteReadTerrain(self) -> None:
        terrain = Terrain("test0",["sert de test","n'existe pas!!"])
        main.writeFile(terrain, True)
        terrainBis = main.readFile("test0","terrain")
        self.assertTrue(terrain == terrainBis)
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
