#pragma once
#include <string>

class XmlRouter {
public:
    explicit XmlRouter(std::string outputRoot);

    // Reads the file, determines target dir from XML content, moves it.
    bool route(const std::string& filePath);

    // Parses XML content and extracts the routing key from a specific tag.
    // Returns "UNSORTED" if the tag is missing or the XML is invalid.
    // Static so it can be unit-tested in isolation.
    static std::string extractKey(const std::string& content);

private:
    std::string outputRoot_;
    static std::string readFile(const std::string& path);
};