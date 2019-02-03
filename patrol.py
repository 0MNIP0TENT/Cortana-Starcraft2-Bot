from sc2.constants import *
import random
def get_forces(self):
    return self.units.exclude_type({SCV,FACTORY}) 

async def patrol_all(self,iteration):
    if iteration % 50 == 0:
        await self.do_actions([unit.move(self.units(COMMANDCENTER).random.position.towards_with_random_angle(self.game_info.map_center, 16)) for unit in get_forces(self).idle])
    if self.supply_used > 190 and self.known_enemy_units.empty:
        await  self.do_actions([unit.move(random.choice(self.enemy_start_locations)) for unit in get_forces(self)])     