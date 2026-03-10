cmake_minimum_required(VERSION 3.10)
project(ClimateSimulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)
file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(test_run test.cpp ${SOURCES})

