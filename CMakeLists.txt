cmake_minimum_required(VERSION 3.10)
project(xml2dir  VERSION 1.0.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)

# Find pugixml
find_package(pugixml REQUIRED)
find_package(Boost 1.66.0 REQUIRED COMPONENTS filesystem system)   

message(STATUS "========== BOOST DEBUG ==========")

execute_process(
    COMMAND sh -c "rpm -qa | grep -i boost | sort"
    OUTPUT_VARIABLE BOOST_RPM_PACKAGES
    ERROR_VARIABLE BOOST_RPM_ERROR
)

message(STATUS "Installed Boost RPM packages:")
message(STATUS "${BOOST_RPM_PACKAGES}")

execute_process(
    COMMAND sh -c "find /usr/lib64 /usr/lib -name 'libboost_filesystem*' -o -name 'libboost_system*' 2>/dev/null"
    OUTPUT_VARIABLE BOOST_LIB_FILES
    ERROR_VARIABLE BOOST_LIB_ERROR
)

message(STATUS "Boost library files:")
message(STATUS "${BOOST_LIB_FILES}")

message(STATUS "=================================")

find_package(Threads REQUIRED)

# Core libraries
add_library(
    xml2dir_core STATIC
    src/Config.cpp
    src/Logger.cpp
    src/FileQueue.cpp
    src/XmlRouter.cpp
    src/Service.cpp
)

target_include_directories(xml2dir_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(xml2dir_core
    PUBLIC
        Threads::Threads
        pugixml::pugixml
        Boost::filesystem
        Boost::system
    )
# Main executable
add_executable(xml2dir src/main.cpp)
target_link_libraries(xml2dir PRIVATE xml2dir_core)

# Tests enabled later
option(BUILD_TESTS "Build tests" OFF)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
install(TARGETS xml2dir RUNTIME DESTINATION bin)