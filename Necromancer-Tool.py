#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random

# Caster info
casterLevel = 9
casterProf = 4

class Weapon:
    Name = ""
    DamageDie = ""
    DamageType = ""
    BonusToHit = 0
    BonusToDmg = 0
    
    def __init__ (self, name, die, dtype, hit, dmg):
        self.Name = name
        self.DamageDie = die
        self.DamageType = dtype
        self.BonusToHit = hit
        self.BonusToDmg = dmg
        
    def __str__ (self):
        return "{4}: +{0} to hit, ({1}) + {2} {3} damage".format(self.BonusToHit, self.DamageDie, self.BonusToDmg, self.DamageType, self.Name)

class DamageRoll:
    crit = False
    hitRoll = 0
    damageRoll = 0
    damageDie = 0
    attacker = None
    
    def __str__ (self):
        return "hit:" + str(self.hitRoll) + " | damageRoll:" + str(self.damageRoll)

class Mob:
    AC = 0
    Health = 0
    Str, Dex, Con, Int, Wis, Chr = 0, 0, 0, 0, 0, 0
    Weapons = []
    EquipWeapon = None
    Icon = "⚫"
    
    def __init__ (self):
        raise NotImplementedError()
        
    def getDamageMod(self):
        raise NotImplementedError()
    
    # Make an attack roll, modify by equip weapon
    def makeAttack(self):
        self.rollClass.attacker = self

        attackRoll = random.randint(1,20)
        if attackRoll == 1:
            self.rollClass.hitRoll = 1
            return 1
        if attackRoll == 20:
            self.rollClass.hitRoll = "crit"
            return "crit"
        
        self.rollClass.hitRoll = attackRoll + self.EquipWeapon.BonusToHit
        return self.rollClass.hitRoll
    
    # Make a strike using equip weapon
    def dealDamage(self):
        splitString = self.EquipWeapon.DamageDie.split("d")
        numAttacks = int(splitString[0])
        maxDamage = int(splitString[1])
        
        damageTotal = 0
        for i in range(0, numAttacks):
            damageTotal = damageTotal + random.randint(1, maxDamage)
        damageTotal = damageTotal + self.EquipWeapon.BonusToDmg
        self.rollClass.damageRoll = damageTotal
        self.rollClass.damageDie = self.EquipWeapon.DamageDie
        return self.rollClass
        
    # Crit using equip weapon!
    def dealCrit(self):
        splitString = self.EquipWeapon.DamageDie.split("d")
        numAttacks = int(splitString[0])
        maxDamage = int(splitString[1])
        
        damageTotal = 0
        for i in range(0, numAttacks*2):
            damageTotal = damageTotal + random.randint(1, maxDamage)
        damageTotal = damageTotal + self.EquipWeapon.BonusToDmg
        
        self.rollClass.damageRoll = damageTotal
        self.rollClass.damageDie = self.EquipWeapon.DamageDie
        self.rollClass.crit = True
        return self.rollClass

class Skel(Mob):
    AC = 13
    Health = 13 + casterLevel
    Icon = "💀"
    
    Str, Dex, Con = 0, 2, 2
    Int, Wis, Chr = -2, -1, -3
    
    def __init__ (self, equip = 0):
        self.rollClass = DamageRoll()
        self.Weapons = []
        
        self.Weapons.append(Weapon("Shortsword", "1d6", "slashing", 4, self.getDamageMod()))
        self.Weapons.append(Weapon("Shortbow", "1d6", "piercing", 4, self.getDamageMod()))
        self.Weapons.append(Weapon("Light Crossbow", "1d8", "piercing", 4, self.getDamageMod()))

        self.EquipWeapon = self.Weapons[equip]


    def __str__ (self):
        return "Skel:\n Equip:" + str(self.EquipWeapon) + "\n Rolls:\n  " + str(self.rollClass)
    
    def getDamageMod(self):
        return self.Dex + casterProf

class Zomb(Mob):
    AC = 8
    Health = 22 + casterLevel
    Icon = "🧟"
    
    Str, Dex, Con = 1, -2, 3
    Int, Wis, Chr = -4, -2, -3
    
    def __init__ (self, equip = 0):
        self.rollClass = DamageRoll()
        self.Weapons = []
        
        self.Weapons.append(Weapon("Slam", "1d6", "bludgeoning", 3, self.getDamageMod()))
        self.EquipWeapon = self.Weapons[equip]

    def __str__ (self):
        return "Zomb:\n Equip:" + str(self.EquipWeapon) + "\n Rolls:\n  " + str(self.rollClass)
    
    def getDamageMod(self):
        return self.Str + casterProf
        
class Ghoul(Mob):
    AC = 12
    Health = 22 + casterLevel
    Icon = "👤"
    
    Str, Dex, Con = 1, 2, 0
    Int, Wis, Chr = -2, 0, -2
    
    def __init__ (self, equip = 0):
        self.rollClass = DamageRoll()
        self.Weapons = []
        
        self.Weapons.append(Weapon("Bite", "2d6", "piercing", 2, self.getDamageMod()))
        self.Weapons.append(Weapon("Claws", "2d4", "slashing", 4, self.getDamageMod()))

        self.EquipWeapon = self.Weapons[equip]

    def __str__ (self):
        return "Ghoul:\n Equip:" + str(self.EquipWeapon) + "\n Rolls:\n  " + str(self.rollClass)
    
    def getDamageMod(self):
        return self.Dex + casterProf
        
# Input: List of mobs, weapons equip and mods set
# During: Asks for target AC
# Purpose: Provide an easy way for a group of mobs to attack a single target
# Output: Prints Total damage to target, roll info
def massAttack(mobs):
    # Input the AC of the target
    print "Please input target 🛡AC:"
    targetAC = input()
    print "Target 🛡AC is " + str(targetAC)
    
    # Go through array, make a roll for each mob in it, store results
    rollArray = []
    numCrits = 0
    for mob in mobArray:
        attackRoll = mob.makeAttack()
        if attackRoll == "crit":
            rollArray.append(mob.dealCrit())
            numCrits = numCrits + 1
        elif attackRoll >= targetAC:
            rollArray.append(mob.dealDamage())
    
    print str(len(rollArray)) + " attacks landed! (" + str(numCrits) + " crits)"        
    
    # Calculate total damage
    totalDamage = 0
    for roll in rollArray:
        totalDamage = totalDamage + roll.damageRoll
    
    # Print roll information
    print "Dealt " + str(totalDamage) + " damage!"
    print " -- == -- == -- == -- == --"
    for roll in rollArray:
        printStr = str(roll.attacker.Icon) + " ⚔" + str(roll.damageRoll) + " [" + str(roll.hitRoll) + "] "
        printStr += str(roll.attacker.EquipWeapon)
        if roll.crit:
            printStr += " 🌟CRIT!"
         
        print printStr


# == -- == -- == -- == -- ==
# Main loop
# == -- == -- == -- == -- ==
print "Please give the number of skellys 💀"
numSkel = input()
print "You have selected " + str(numSkel) + " to be your size"

print "Please give the number of zombs 🧟️"
numZomb = input()
print "You have selected " + str(numZomb) + " to be your size"

print "Please give the number of ghouls 👤️"
numGhoul = input()
print "You have selected " + str(numGhoul) + " to be your size"

# Make a number of mobs equal to input, add to array
mobArray = []
for i in range (0, numSkel):
    newSkel = Skel(2)
    mobArray.append(newSkel)
    
for i in range (0, numZomb):
    newZomb = Zomb(0)
    mobArray.append(newZomb)
    
for i in range (0, numGhoul):
    newGhoul = Ghoul(1)
    mobArray.append(newGhoul)




# ATTACK!!!
massAttack(mobArray)
