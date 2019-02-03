import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.ids.unit_typeid import COMMANDCENTER, SUPPLYDEPOT, SCV, BARRACKS,REFINERY, FACTORY,CYCLONE,FACTORYTECHLAB
from sc2.constants import *
from sc2.player import Bot, Computer, Human
import training, building, assault,patrol


class Cortana(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()

        if self.can_afford(COMMANDCENTER) and self.units(COMMANDCENTER).amount < 2:
            await self.expand_now()
        elif self.can_afford(COMMANDCENTER) and self.units(COMMANDCENTER).amount < 2 and self.supply_used > 140:
            await self.expand_now()    

        await building.build_buildings(self)

        await training.train_army(self)
        if self.supply_used > 180:
            await assault.attack_all(self)

        await patrol.patrol_all(self,iteration)

def main():
    run_game(maps.get("HonorgroundsLE"), [
        #Human(Race.Terran),
        Bot(Race.Terran, Cortana()),
        Computer(Race.Zerg, Difficulty.Medium)
    ], realtime=True)

if __name__ == '__main__':
    main()