#include <algorithm>
#include <any>
#include <cmath>
#include <cstddef>
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

struct SimulationResult {
    std::vector<double> theta_angles;
    std::vector<double> temperatures;
    std::vector<WaterState> water_phases;
    double habitability;
};

class Calculator {
	private:
    const double sigma_const = 5.67e-8;
    const double G_const = 6.67430e-11;
    
    const double M_earth = 5.972e24;  
    const double R_earth = 6371000.0; 
    const double g_earth = 9.81;      

	public:
    double radians(const double angle_degrees) const {
        return angle_degrees * M_PI / 180.0;
    }

	public:
    double surface_gravity(Planet &planet) const {
        double real_mass_kg = planet.get_mass() * M_earth;
        double real_radius_m = planet.get_radius() * R_earth;
        return G_const * real_mass_kg / std::pow(real_radius_m, 2);
    }

	public:
    double surface_pressure(Planet &planet) const {
        return planet.get_base_pressure() * (planet.get_mass() / std::pow(planet.get_radius(), 2));    
    }

	public:
    double boiling_temp(Planet &planet) const {
        return 373.15 + 28.0 * std::log(surface_pressure(planet) / 1.0);
    }

	public:
    double diffusion_coeff(Planet &planet) const {
        double gravity_ratio = surface_gravity(planet) / g_earth;
        return planet.get_base_diffusion() * (planet.get_base_pressure() * gravity_ratio);
    }

	public:
    double heat_in(Planet &planet, Star &star, const double angle_degrees) const {
        return (star.get_stellar_flux() / M_PI) * (1.0 - planet.get_albedo()) * std::max(0.0, std::sin(radians(angle_degrees)));
    }

	public:
    double heat_out(Planet &planet, const double current_temperature) const {
        return planet.get_emissivity() * sigma_const * std::pow(current_temperature, 4);
    }

	public:
    double heat_transport(const double diffusion_coeff, const double temp_left, 
                          const double temp_right, const double temp_current) const {
        return diffusion_coeff * ((temp_left - temp_current) + (temp_right - temp_current));
    }

	public:
    double calculate_new_temperature(const double temp_current, const double delta_t, 
                                     const double heat_capacity, const double incoming_heat, 
                                     const double outgoing_heat, const double transport_heat) const {
        return temp_current + (delta_t / heat_capacity) * (incoming_heat - outgoing_heat + transport_heat);
    }
};

class ClimateEngine {
	private:
    Calculator calc; 
    size_t grid_size;
    
	private:
    std::vector<double> theta_angles;
    std::vector<double> current_temperatures;
    std::vector<double> next_temperatures;
    
	public:
    ClimateEngine(const size_t size = 180) {
        this->grid_size = size;

        theta_angles.resize(size);
        current_temperatures.resize(size);
        next_temperatures.resize(size);

        double step_size = 180.0 / (size - 1); 
        for (size_t i = 0; i < size; i++) {
            theta_angles[i] = i * step_size;
        }

        std::fill(current_temperatures.begin(), current_temperatures.end(), 280.0);
    }

	public:
    SimulationResult run_simulation(Planet &planet, Star &star, 
			const double delta_t, const double total_steps = 10000) {
        SimulationResult result;

        const double boiling_temperature = calc.boiling_temp(planet);
        const double diffusion_coefficient = calc.diffusion_coeff(planet);

        for (size_t step = 0; step < total_steps; step++) {
            
            for (size_t i = 0; i < grid_size; i++) {
                
                double temperature_left; 
				if (i > 0) {
					temperature_left = current_temperatures[i - 1];
				} else {
					temperature_left = current_temperatures[i];
				}

                double temperature_right; 
				if (i < grid_size - 1) {
					temperature_right = current_temperatures[i + 1];
				} else {
					temperature_right = current_temperatures[i];
				}

                const double incoming_heat = calc.heat_in(planet, star, theta_angles[i]);
                const double outgoing_heat = calc.heat_out(planet, current_temperatures[i]);
                const double transport_heat = calc.heat_transport(diffusion_coefficient, temperature_left, 
                                                            temperature_right, current_temperatures[i]);

                next_temperatures[i] = calc.calculate_new_temperature(
                    current_temperatures[i], delta_t, planet.get_heat_capacity(), 
                    incoming_heat, outgoing_heat, transport_heat
                );
            }

            current_temperatures = next_temperatures;
        }

        for (const auto &temperature : current_temperatures) {
            if (temperature <= 273.15) {
                result.water_phases.push_back(WaterState::Solid);
            } else if (temperature >= boiling_temperature) {
                result.water_phases.push_back(WaterState::Gas);
            } else {
                result.water_phases.push_back(WaterState::Liquid);
            }
        }

        double sum_zone_weight = 0.0;
        double sum_zone_weight_liquid = 0.0;
        
        for (size_t i = 0; i < grid_size; i++) {
            double zone_weight = std::sin(calc.radians(theta_angles[i]));
            sum_zone_weight += zone_weight;

            if (result.water_phases[i] == WaterState::Liquid) {
                sum_zone_weight_liquid += zone_weight;
            }
        }

        if (sum_zone_weight > 0.0) {
            result.habitability = (sum_zone_weight_liquid / sum_zone_weight) * 100.0;
        } else {
            result.habitability = 0.0;
        }
        
        result.temperatures = next_temperatures;
        result.theta_angles = theta_angles;
        
        return result;
    }
};

