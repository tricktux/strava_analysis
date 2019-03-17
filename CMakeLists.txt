# File:           CMakeLists.txt
# Description:     Code Description
# Author:		    Reinaldo Molina
# Email:          rmolin88 at gmail dot com
# Revision:	    0.0.0
# Created:        Tue Mar 05 2019 06:13
# Last Modified:  Tue Mar 05 2019 06:13

cmake_minimum_required(VERSION 3.1)

# Set ProjectName
project(strava_analysis)

option(USE_CLANG "build application with clang" ON) # ON is the default

if (USE_CLANG)
	SET (CMAKE_CXX_COMPILER "/usr/bin/clang++" )
	SET (CMAKE_AR           "/usr/bin/llvm-ar" )
	SET (CMAKE_LINKER       "/usr/bin/llvm-ld" )
	SET (CMAKE_NM           "/usr/bin/llvm-nm" )
	SET (CMAKE_OBJDUMP      "/usr/bin/llvm-objdump" )
	SET (CMAKE_RANLIB       "/usr/bin/llvm-ranlib" )
endif (USE_CLANG)


# if(NOT CMAKE_BUILD_TYPE)
	# set(CMAKE_BUILD_TYPE "Release" CACHE STRING
		# "Choose the type of build, options are: Debug Release
		# RelWithDebInfo MinSizeRel."
		# FORCE)
# endif(NOT CMAKE_BUILD_TYPE)

# Specify output directories.
set(EXECUTABLE_OUTPUT_PATH "${PROJECT_BINARY_DIR}/bin")

# Include custom macros to find Glog.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
	"${CMAKE_CURRENT_SOURCE_DIR}/cmake")

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

find_package(RapidJSON REQUIRED)

find_package(GLog REQUIRED)

find_package(GTest REQUIRED)

include(FindPkgConfig)
pkg_check_modules(CURLPP REQUIRED curlpp)

# Build with c++17 support
set(CMAKE_CXX_STANDARD 17)

add_subdirectory("src")

option(ENABLE_TESTS "Build tests" OFF)
if(ENABLE_TESTS)
	enable_testing()
	add_subdirectory("tests")
endif()
