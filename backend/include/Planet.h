#include "planet_errors/all_planet_errors.h"

class Planet {
	private:
	double mass; 
	double radius;
	double albedo;
	double emissivity; 
	double heat_capacity;
	double base_pressure; 
	double base_diffusion; 

	// reference is just a pointer, a pointer 
	// on a 64 bit system is 8 bytes, a double
	// is also 8 bytes, so it doesn't matter
	public:
	void set_mass            (const double mass);
	void set_radius          (const double radius);
	void set_albedo          (const double albedo);
	void set_emissivity      (const double emissivity);
	void set_heat_capacity   (const double heat_capacity);
	void set_base_pressure   (const double base_pressure);
	void set_base_diffusion  (const double base_diffusion);

	public:
	double get_mass()           const;
	double get_radius()         const;
	double get_albedo()         const;
	double get_emissivity()     const;
	double get_heat_capacity()  const;
	double get_base_pressure()  const; 
	double get_base_diffusion() const;

	public:
	Planet();
};

