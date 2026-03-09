#include "../../include/planet_errors/empty_planet_argument.h"

EmptyPlanetArgument::EmptyPlanetArgument(const PlanetParameter parameter_type) {
	this->parameter_type = parameter_type;
	
	error = "Empty argument! ";
	switch (parameter_type) {
		case PlanetParameter::mass:
			error += "mass";
			break;
		case PlanetParameter::radius:
			error += "radius";
			break;
		case PlanetParameter::albedo:
			error += "albedo";
			break;
		case PlanetParameter::emissivity:
			error += "emissivity";
			break;
		case PlanetParameter::heat_capacity:
			error += "heat_capacity";
			break;
		case PlanetParameter::base_diffusion:
			error += "base_diffusion";
			break;
		case PlanetParameter::base_pressure:
			error += "base_pressure";
			break;
	}

	error += " is NaN.";
}

const char * EmptyPlanetArgument::what() const noexcept {
	return error.c_str();
}

