cmake_minimum_required(VERSION 3.20)
project(vessel_geo CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(VTK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/deps/vtk/lib/cmake/vtk-9.3"
    CACHE PATH "Path to vtk-config.cmake")

set(CGAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/deps/cgal/lib/cmake/CGAL"
    CACHE PATH "Path to CGALConfig.cmake")

find_package(CGAL REQUIRED)
find_package(TBB REQUIRED)

find_package(VTK REQUIRED COMPONENTS
    CommonCore
    CommonDataModel
    IOXML
    FiltersCore
    IOPLY
)

add_executable(vessel_geo
    src/main.cpp
)

target_include_directories(vessel_geo PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

target_link_libraries(vessel_geo PRIVATE
    CGAL::CGAL
    VTK::CommonCore
    VTK::CommonDataModel
    VTK::IOXML
    VTK::FiltersCore
    VTK::IOPLY
)

vtk_module_autoinit(
    TARGETS vessel_geo
    MODULES VTK::CommonCore VTK::CommonDataModel VTK::IOXML VTK::FiltersCore VTK::IOPLY
)
