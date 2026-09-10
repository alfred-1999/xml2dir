cmake_minimum_required(VERSION 3.10)
project(xml2dir CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find pugixml
find_package(pugixml REQUIRED)

# Core libraries
add_library(
    xml2dir_core
    src/Config.cpp
    src/Logger.cpp
    src/FileQueue.cpp
    src/XmlRouter.cpp
    src/Service.cpp
)

target_include_directories(xml2dir_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
find_package(Threads REQUIRED)
target_link_libraries(xml2dir_core PUBLIC Threads::Threads pugixml::pugixml)

# Tests enabled later
option(BUILD_TESTS "Build tests" OFF)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
install(TARGETS xml2dir RUNTIME DESTINATION bin)