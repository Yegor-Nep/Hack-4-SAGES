#pragma once

#include <cstdint>

enum class PlanetParameter: uint8_t {
	mass,
	radius,
	albedo,
	emissivity,
	heat_capacity,
	base_pressure,
	base_diffusion,
};

