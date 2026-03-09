#include "../include/Planet.h"
#include <cmath>
#include <limits>

void Planet::set_mass(const double mass) {
	if (mass < 0 or mass > 10) {
		throw InvalidPlanetSetArgument(PlanetParameter::mass, mass);		
	}

	this->mass = mass;
}

void Planet::set_radius(const double radius) {
	if (radius < 0.5 or radius > 2.5) {
		throw InvalidPlanetSetArgument(PlanetParameter::radius, radius);
	}

	this->radius = radius;
}

void Planet::set_albedo(const double albedo) {
	if (albedo < 0 or albedo > 1) {
		throw InvalidPlanetSetArgument(PlanetParameter::albedo, albedo);
	}

	this->albedo = albedo;
}

void Planet::set_emissivity(const double emissivity) {
	if (emissivity < 0.01 or emissivity > 1) {
		throw InvalidPlanetSetArgument(PlanetParameter::emissivity, emissivity);
	}

	this->emissivity = emissivity;
}

void Planet::set_heat_capacity(const double heat_capacity) {
	if (heat_capacity < 1000000 or heat_capacity > 100000000) {
		throw InvalidPlanetSetArgument(PlanetParameter::heat_capacity, heat_capacity);
	}

	this->heat_capacity = heat_capacity;
}

void Planet::set_base_diffusion(const double base_diffusion) {
	if (base_diffusion < 0 or base_diffusion > 10)  {
		throw InvalidPlanetSetArgument(PlanetParameter::base_diffusion, base_diffusion);
	}

	this->base_diffusion = base_diffusion;
}

void Planet::set_base_pressure(const double base_pressure) {
	if (base_pressure < 0.01 or base_pressure > 100) {
		throw InvalidPlanetSetArgument(PlanetParameter::base_pressure, base_pressure);
	}
}

double Planet::get_mass() const {
	if (std::isnan(mass)) {
		throw EmptyPlanetArgument(PlanetParameter::mass);
	}

	return mass;
}

double Planet::get_radius() const {
	if (std::isnan(radius)) {
		throw EmptyPlanetArgument(PlanetParameter::radius);
	}

	return mass;
}

double Planet::get_albedo() const {
	if (std::isnan(albedo)) {
		throw EmptyPlanetArgument(PlanetParameter::albedo);
	}

	return mass;
}

double Planet::get_emissivity() const {
	if (std::isnan(emissivity)) {
		throw EmptyPlanetArgument(PlanetParameter::emissivity);
	}

	return mass;
}

double Planet::get_heat_capacity() const {
	if (std::isnan(heat_capacity)) {
		throw EmptyPlanetArgument(PlanetParameter::heat_capacity);
	}

	return mass;
}

double Planet::get_base_diffusion() const {
	if (std::isnan(base_diffusion)) {
		throw EmptyPlanetArgument(PlanetParameter::base_diffusion);
	}

	return base_diffusion;
}

double Planet::get_base_pressure() const {
	if (std::isnan(base_pressure)) {
		throw EmptyPlanetArgument(PlanetParameter::base_pressure);
	}

	return base_pressure;
}

Planet::Planet() {
	mass           = std::numeric_limits<double>::quiet_NaN();
	radius         = std::numeric_limits<double>::quiet_NaN();
	albedo         = std::numeric_limits<double>::quiet_NaN();
	emissivity     = std::numeric_limits<double>::quiet_NaN();
	heat_capacity  = std::numeric_limits<double>::quiet_NaN();
	base_pressure  = std::numeric_limits<double>::quiet_NaN();
	base_diffusion = std::numeric_limits<double>::quiet_NaN();
}

