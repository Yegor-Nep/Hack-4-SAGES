#pragma once

#include <stdexcept>
#include <string>
#include "star_parameter_type.h"

class EmptyStarArgument : public std::exception {
	private:
	StarSetArgument parameter_type;
	double parameter;
	std::string error;

	public:
	EmptyStarArgument(const StarSetArgument parameter_type, double parameter);

	public:
	const char * what() const noexcept override;
};

