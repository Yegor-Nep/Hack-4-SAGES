from enum import Enum

import sys
sys.path.insert(1, '../frontend')
from params_enum import Parametrs

import cpp_heat_engine

class Facade:
    data = {}
    def __init__(self):
        self.data = {} 
        self.planet = cpp_heat_engine.Planet()
        self.star = cpp_heat_engine.Star()
        self.engine = cpp_heat_engine.ClimateEngine(180)

    def run_simulation(self):
        self.planet.set_mass(self.data[Parametrs.mass])
        self.planet.set_radius(self.data[Parametrs.radius])
        self.planet.set_albedo(self.data[Parametrs.albedo])
        self.planet.set_emissivity(self.data[Parametrs.emissivity])
        self.planet.set_heat_capacity(self.data[Parametrs.heat_capacity])
        self.planet.set_base_diffusion(self.data[Parametrs.base_diffusion])
        self.planet.set_base_pressure(self.data[Parametrs.base_pressure])

        self.star.set_stellar_flux(self.data[Parametrs.stellar_flux])

        simulation = self.engine.run_simulation(self.planet, self.star, 5000, 10000)
        
        return_dict = {}
        return_dict["theta_angles"] = simulation.theta_angles
        return_dict["temperatures"] = simulation.temperatures
        return_dict["water_phases"] = [phase.name for phase in simulation.water_phases]
        return_dict["habitability"] = simulation.habitability

        return return_dict

    # GETTERS SETTERS
    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


def test():
    import random

    random_test_data = {
        Parametrs.mass: random.uniform(0.1, 10.0),
        Parametrs.radius: random.uniform(0.5, 2.5),
        Parametrs.albedo: random.uniform(0.0, 1.0),
        Parametrs.emissivity: random.uniform(0.01, 1.0),
        Parametrs.heat_capacity: random.uniform(1000000.0, 100000000.0),
        Parametrs.base_diffusion: random.uniform(0.0, 100.0),
        Parametrs.base_pressure: random.uniform(0.01, 100.0),
        Parametrs.stellar_flux: random.uniform(100.0, 3000.0)
    }

    earth_test_data = {
        Parametrs.mass: 1.0,
        Parametrs.radius: 1.0,
        Parametrs.albedo: 0.3,
        Parametrs.emissivity: 0.6,
        Parametrs.heat_capacity: 10000000.0,
        Parametrs.base_diffusion: 8.0,
        Parametrs.base_pressure: 1.0,
        Parametrs.stellar_flux: 1361.0
    }

    test_facade = Facade()
    test_facade.set_data(earth_test_data) 
    results = test_facade.run_simulation()
    print(results)

# test()

facade_singleton = Facade()

