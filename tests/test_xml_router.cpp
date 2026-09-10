#include <gtest/gtest.h>
#include "xml2dir/XmlRouter.hpp"

TEST(ExtractKey, RoutesToA) {
    std::string xml = R"(<message><route>A</route></message>)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "A");
}

TEST(ExtractKey, RoutesToB) {
    std::string xml = R"(<message><route>B</route></message>)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "B");
}

TEST(ExtractKey, TrimsWhitespace) {
    std::string xml = R"(<message><route>  A  </route></message>)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "A");
}

TEST(ExtractKey, MissingTagIsUnsorted) {
    std::string xml = R"(<message><other>X</other></message>)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "UNSORTED");
}

TEST(ExtractKey, EmptyTagIsUnsorted) {
    std::string xml = R"(<message><route></route></message>)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "UNSORTED");
}

TEST(ExtractKey, InvalidXmlIsUnsorted) {
    std::string xml = R"(this is not xml <<<)";
    EXPECT_EQ(XmlRouter::extractKey(xml), "UNSORTED");
}