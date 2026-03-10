#include "../../include/star_errors/empty_star_argument.h"

EmptyStarArgument::EmptyStarArgument(const StarSetArgument parameter_type, double parameter) {
	this->parameter_type = parameter_type;

	error = "Empty argument! ";
	switch (parameter_type) {
		case StarSetArgument::stellar_flux:
			error += "stellar_flux";
			break;
	}

	error += " is NaN.";
}

const char * EmptyStarArgument::what() const noexcept {
	return error.c_str();
}

