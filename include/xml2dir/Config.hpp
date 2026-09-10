#pragma once
#include <string>

struct Config {
    std::string queueDir;
    std::string outputRoot;
    std::string logFile;
    int pollIntervalMs = 1000; // Default to 1000 milliseconds

    // Load from a simple key=value configuration file. Returns true if successful, false otherwise.
    static bool load(const std::string& path, Config& out);
};