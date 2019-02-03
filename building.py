from sc2.ids.unit_typeid import SUPPLYDEPOT, COMMANDCENTER, SCV, BARRACKS, REFINERY, FACTORY, FACTORYTECHLAB, FACTORYREACTOR, STARPORT

async def supply_up(self):
    if self.supply_left < 10 and self.supply_used < 200:
        if self.can_afford(SUPPLYDEPOT):
            await self.build(SUPPLYDEPOT, near=command_centers(self).first.position.towards_with_random_angle(self.game_info.map_center, 8))

def command_centers(self):
    return self.units(COMMANDCENTER)

async def train_workers(self):
    if command_centers(self).exists:
        cc = command_centers(self).random
        if self.units(SCV).amount < command_centers(self).amount * 16:
            if self.can_afford(SCV) and cc.noqueue:
                await self.do(cc.train(SCV))

async def build_refinery(self):
    if self.units(BARRACKS).exists and self.units(REFINERY).amount < 2:
        if self.can_afford(REFINERY):
            vgs = self.state.vespene_geyser.closer_than(20.0, command_centers(self).random)
            for vg in vgs:
                if self.units(REFINERY).closer_than(1.0, vg).exists:
                    break
                worker = self.select_build_worker(vg.position)
                if worker is None:
                    break
                await self.do(worker.build(REFINERY, vg))
                break

async def build_barracks(self):
    if self.units(SUPPLYDEPOT).ready.exists and self.units(BARRACKS).amount < 1:
        if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
            await self.build(BARRACKS, near=command_centers(self).random.position.towards(self.game_info.map_center, 16))

async def build_factory(self):
        if self.units(BARRACKS).ready.exists and self.can_afford(FACTORY) and self.units(FACTORY).amount < 3:
            if not self.already_pending(FACTORY):
                await self.build(FACTORY, near=command_centers(self).random.position.towards_with_random_angle(self.game_info.map_center, 16))

async def factory_attachments(self):
    if self.units(FACTORY).ready:
        for factory in self.units(FACTORY).ready:
            if self.can_afford(FACTORYTECHLAB) and factory.add_on_tag == 0 and self.can_place(FACTORYTECHLAB, factory.position) and self.units(FACTORY).amount < 3:
                await self.do(factory.build(FACTORYTECHLAB, factory.add_on_land_position)) 
            elif self.units(FACTORY).amount >= 3 and factory.add_on_tag == 0 and self.can_afford(FACTORYREACTOR):
                await self.do(factory.build(FACTORYREACTOR, factory.add_on_land_position)) 

async def build_starport(self):
    if self.units(BARRACKS).exists and self.units(STARPORT).amount < 3:
        if self.can_afford(STARPORT):
            await self.build(FACTORY, near=command_centers(self).random.position.towards_with_random_angle(self.game_info.map_center, 16))

async def build_buildings(self):
    await supply_up(self)    
    await train_workers(self)
    await build_refinery(self)
    await build_barracks(self)
    await build_factory(self)
    await build_starport(self)
    await factory_attachments(self)                