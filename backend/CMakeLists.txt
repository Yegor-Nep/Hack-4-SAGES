cmake_minimum_required(VERSION 3.10)
project(ClimateSimulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

include_directories(include)
file(GLOB_RECURSE SOURCES "src/*.cpp")

pybind11_add_module(cpp_heat_engine build_file.cpp ${SOURCES})

