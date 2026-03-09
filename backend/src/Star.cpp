#include "../include/Star.h"
#include <cmath>
#include <limits>

void Star::set_stellar_flux(double stellar_flux) {
	if (stellar_flux > 3000 or stellar_flux < 100) {
		throw InvalidStarSetArgument(StarSetArgument::stellar_flux, stellar_flux);
	}

	this->stellar_flux = stellar_flux;
}

double Star::get_stellar_flux() const {
	if (std::isnan(stellar_flux)) {
		throw EmptyStarArgument(StarSetArgument::stellar_flux, stellar_flux);
	}

	return stellar_flux;
}

Star::Star() {
	stellar_flux = std::numeric_limits<double>::quiet_NaN();
}

