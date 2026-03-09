#pragma once

#include <stdexcept>
#include <string>
#include "planet_parameter_type.h"

class InvalidPlanetSetArgument : public std::exception {
	private:
	PlanetParameter parameter_type;
	double parameter;
	std::string error;

	public:
	InvalidPlanetSetArgument(const PlanetParameter parameter_type, double parameter);

	public:
	const char * what() const noexcept override;
};

