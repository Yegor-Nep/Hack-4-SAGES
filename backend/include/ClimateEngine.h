#include <cmath>
#include <cstdint>
#include <vector>

#include "Planet.h"
#include "Star.h"

// uint8_t for better caching memory handling
// here actuall difference as the simulation
// will use these enums a shit ton and uint8_t
// takes up 4x less memory than default int  
enum class WaterState : uint8_t { 
	Liquid, Gas, Solid	
};

class ClimateEngine {
	private:
	std::vector<double> theta_angles; 
	std::vector<double> temperatures; 
	std::vector<WaterState> water_phases; 

	// consts
	private:
	const double sigma_const = 5.67e-8;
    const double G_const = 6.67430e-11;

	private:
	double calculate_surface_gravity(const Planet &planet) {
		return G_const * planet.get_mass() / std::pow(planet.get_radius(), 2);
	}

	private:
	double calculate_surface_preassure(const Planet &planet) {
	}

	public:
	void run_simulation() {
	}
};

