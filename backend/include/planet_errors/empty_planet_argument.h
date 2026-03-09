#pragma once

#include <exception>
#include <string>
#include "planet_parameter_type.h"

class EmptyPlanetArgument : public std::exception {
	private:
	PlanetParameter parameter_type;
	std::string error;

	public:
	EmptyPlanetArgument(const PlanetParameter parameter_type);

	public:
	const char * what() const noexcept override;
};

