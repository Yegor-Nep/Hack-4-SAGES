#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 

#include "include/ClimateEngine.h"

namespace py = pybind11;

PYBIND11_MODULE(cpp_heat_engine, m) {
    m.doc() = "C++ 1D Climate Engine for Exoplanet Simulation";

    py::enum_<WaterState>(m, "WaterState")
        .value("Liquid", WaterState::Liquid)
        .value("Gas", WaterState::Gas)
        .value("Solid", WaterState::Solid)
        .export_values();

    py::class_<SimulationResult>(m, "SimulationResult")
        .def(py::init<>()) 
        .def_readwrite("theta_angles", &SimulationResult::theta_angles)
        .def_readwrite("temperatures", &SimulationResult::temperatures)
        .def_readwrite("water_phases", &SimulationResult::water_phases)
        .def_readwrite("habitability", &SimulationResult::habitability);

    py::class_<Planet>(m, "Planet")
        .def(py::init<>())
        .def("set_albedo", &Planet::set_albedo)
        .def("set_emissivity", &Planet::set_emissivity)
        .def("set_base_pressure", &Planet::set_base_pressure)
        .def("set_base_diffusion", &Planet::set_base_diffusion)
        .def("set_heat_capacity", &Planet::set_heat_capacity)
        .def("set_mass", &Planet::set_mass)
        .def("set_radius", &Planet::set_radius);

    py::class_<Star>(m, "Star")
        .def(py::init<>())
        .def("set_stellar_flux", &Star::set_stellar_flux);

    py::class_<ClimateEngine>(m, "ClimateEngine")
        .def(py::init<size_t>(), py::arg("size") = 180)
        .def("run_simulation", &ClimateEngine::run_simulation, 
             py::arg("planet"), py::arg("star"), py::arg("delta_t"), py::arg("total_steps") = 10000);
}
