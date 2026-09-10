#include <xml2dir/Config.hpp>
#include <sstream>
#include <fstream>

// Trim whitespace from both ends of a string
static std::string trim(const std::string& s) {
    size_t a = s.find_first_not_of(" \t\r\n");  // Find the first non-whitespace character
    size_t b = s.find_last_not_of(" \t\r\n");   // Find the last non-whitespace character

    if (a == std::string::npos || b == std::string::npos) return "";    // If the string is all whitespace, return an empty string
    return s.substr(a, b - a + 1);  // Return the substring that excludes leading and trailing whitespace
}

bool Config::load(const std::string& path, Config& out) {
    std::ifstream file(path);  // Open the configuration file for reading
    if (!file.is_open()) return false;

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;
        auto eq = line.find('=');
        if (eq == std::string::npos) continue;
        std::string key = trim(line.substr(0, eq));
        std::string val = trim(line.substr(eq + 1));

        if (key == "queueDir")            out.queueDir = val;
        else if (key == "outputRoot")     out.outputRoot = val;
        else if (key == "logFile")        out.logFile = val;
        else if (key == "pollIntervalMs") out.pollIntervalMs = std::stoi(val);
    }
    return true;
}