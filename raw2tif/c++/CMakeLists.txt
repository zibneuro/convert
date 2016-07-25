project(raw2tif)

cmake_minimum_required(VERSION 2.6)

find_package(VTK)

file(GLOB  CPP  *.cpp)

include(${VTK_USE_FILE})

if(CMAKE_COMPILER_IS_GNUCC)
  set (CMAKE_CXX_FLAGS "-std=c++11")
endif(CMAKE_COMPILER_IS_GNUCC)

link_libraries(${VTK_LIBRARIES})

if(MSVC)
  add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif(MSVC)

add_executable(raw2tif
  ${CPP}
)
