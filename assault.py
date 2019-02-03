from sc2.constants import *
import random

def get_forces(self):
    return self.units.exclude_type({SCV}) 

def get_enemy_units(self):
    return self.known_enemy_units.not_structure

def get_enemy_structures(self):
    return self.known_enemy_units.structure    

async def attack_units(self):
    if get_enemy_units(self).exists:
        await self.do_actions(list(map(lambda u: u.attack(get_enemy_units(self).closest_to(get_forces(self).center)),get_forces(self))))

async def attack_structures(self):
    if get_enemy_units(self).empty and get_enemy_structures(self).exists:
        await self.do_actions(list(map(lambda u: u.attack(get_enemy_structures(self).closest_to(get_forces(self).center)),get_forces(self))))       

async def attack_all(self):
    await attack_units(self)
    await attack_structures(self)        