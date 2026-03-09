#include "star_errors/all_stars_errors.h"

class Star {
	private:
	double stellar_flux; 

	// double == 8 bytes == double&
	public:
	void set_stellar_flux(double stellar_flux);

	public:
	double get_stellar_flux() const;

	public:
	Star();
};

