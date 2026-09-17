#include "xml2dir/XmlRouter.hpp"
#include "xml2dir/Logger.hpp"
#include <pugixml.hpp>
#include <boost/filesystem.hpp>
#include <fstream>
#include <sstream>

namespace fs = boost::filesystem;

XmlRouter::XmlRouter(std::string outputRoot) : outputRoot_(std::move(outputRoot)) {}

std::string XmlRouter::readFile(const std::string& path) {
    std::ifstream in(path);
    std::ostringstream ss;
    ss << in.rdbuf();
    return ss.str();
}

std::string XmlRouter::extractKey(const std::string& content) {
    pugi::xml_document doc;
    pugi::xml_parse_result result = doc.load_string(content.c_str());

    if (!result) {
        // Invalid XML — cannot route reliably.
        return "UNSORTED";
    }

    // Look for <message><route>...</route></message>.
    // Adjust the XPath to match YOUR real schema.
    pugi::xpath_node node = doc.select_node("/message/route");
    if (!node) {
        return "UNSORTED";
    }

    std::string key = node.node().child_value();

    // Trim whitespace.
    auto a = key.find_first_not_of(" \t\r\n");
    auto b = key.find_last_not_of(" \t\r\n");
    if (a == std::string::npos) return "UNSORTED";
    key = key.substr(a, b - a + 1);

    return key.empty() ? "UNSORTED" : key;
}

bool XmlRouter::route(const std::string& filePath) {
    std::string content = readFile(filePath);
    if (content.empty()) {
        LOG_WARNING("Empty or unreadable file: " + filePath);
        return false;
    }

    std::string key = extractKey(content);
    fs::path targetDir = fs::path(outputRoot_) / key;

    boost::system::error_code ec;
    fs::create_directories(targetDir, ec);
    if (ec) {
        LOG_ERROR("Cannot create dir " + targetDir.string() + ": " + ec.message());
        return false;
    }

    fs::path target = targetDir / fs::path(filePath).filename();

    if (fs::exists(target)) {
        LOG_INFO("Already exists, skipping: " + target.string());
        fs::remove(filePath, ec);
        return true;
    }

    fs::rename(filePath, target, ec);
    if (ec) {
        LOG_ERROR("Failed to move " + filePath + " -> " + target.string() +
                  ": " + ec.message());
        return false;
    }

    LOG_INFO("Routed " + filePath + " -> " + target.string());
    return true;
}