from sc2.constants import *

async def train_army(self):
    for factory in self.units(FACTORY).noqueue:
        if factory.has_add_on:
            if self.units(CYCLONE).amount <= self.units(SIEGETANK).amount:
                if self.can_afford(CYCLONE):
                    await self.do(factory.train(CYCLONE))
            else:
                if self.can_afford(SIEGETANK):
                    await self.do(factory.train(SIEGETANK))  
    await train_marines(self)           
    await train_hellions(self)
    await train_thors(self)       
    await train_vikings(self)

async def train_marines(self):
    if self.units(BARRACKS).ready.exists:
        await self.do_actions([bar.train(MARINE) for bar in self.units(BARRACKS).noqueue if self.can_afford(MARINE)])                    

async def train_hellions(self):
    await self.do_actions([fac.train(HELLION) for fac in self.units(FACTORY).noqueue if self.can_afford(HELLION)])

async def train_thors(self):
    if self.units(FACTORY).ready.exists:
        await self.do_actions([fac.train(THOR) for fac in self.units(FACTORY).noqueue if self.can_afford(THOR)]) 

async def train_vikings(self):
    if self.units(STARPORT).ready.exists:
        await self.do_actions([star.train(VIKING) for star in self.units(STARPORT).noqueue if self.can_afford(VIKING)]) 
