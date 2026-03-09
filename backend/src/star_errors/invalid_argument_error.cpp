#include "../../include/star_errors/invalid_star_set_argument.h"
#include <string>

InvalidStarSetArgument::InvalidStarSetArgument(const StarSetArgument parameter_type, double parameter) {
	this->parameter_type = parameter_type;
	this->parameter = parameter;

	error += "Invalid value parameter: " + std::to_string(parameter) + " <- ";
	switch (parameter_type) {
		case StarSetArgument::stellar_flux:
			error += "stellar_flux. stellar_flux has to be [100.0; 3000.0]";
			break;
	}	
}

const char * InvalidStarSetArgument::what() const noexcept {
	return error.c_str();
}

