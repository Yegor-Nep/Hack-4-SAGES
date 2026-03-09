#include "../../include/planet_errors/invalid_planet_set_argument.h"
#include <string>

InvalidPlanetSetArgument::InvalidPlanetSetArgument(const PlanetParameter parameter_type, double parameter) {
	this->parameter_type = parameter_type;
	this->parameter = parameter;

	error += "Invalid value parameter: " + std::to_string(parameter) + " <- "; 
	switch (parameter_type) {
		case PlanetParameter::mass:
			error += "mass. mass has to be [0.1; 10.0] (in earth masses)";
			break;
		case PlanetParameter::radius:
			error += "radius. radius has to be [0.5; 2.5] (in earth radiuses)";
			break;
		case PlanetParameter::albedo:
			error += "albedo. albedo has to be [0; 1]";
			break; 
		case PlanetParameter::emissivity:
			error += "emissivity. emissivity has to be [0.01; 1.0]";
			break;
		case PlanetParameter::heat_capacity:
			error += "heat_capacity. heat_capacity has to be [1 000 000; 100 000 000] (in J/m^2*K)";
			break;
		case PlanetParameter::base_diffusion:
			error += "base_diffusion. base_diffusion has to be [0.0; 10.0]";
			break;
		case PlanetParameter::base_pressure:
			error += "base_pressure. base_pressure has to be [0.01; 100.0]";
			break;
	}	
}

const char * InvalidPlanetSetArgument::what() const noexcept {
	return error.c_str();
}

