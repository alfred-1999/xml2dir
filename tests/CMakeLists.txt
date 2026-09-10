find_package(GTest REQUIRED)

add_executable(xml2dir_tests
    test_xml_router.cpp
)
target_link_libraries(xml2dir_tests
    PRIVATE
        xml2dir_core
        GTest::gtest_main
)

add_test(NAME xml2dir_tests COMMAND xml2dir_tests)