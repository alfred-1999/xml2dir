#pragma once
#include <string>
#include <vector>

// Scans a directory for *.xml files.
class FileQueue {
public:
    explicit FileQueue(std::string queueDir);
    // Returns paths of pending .xml files.
    std::vector<std::string> pending() const;

private:
    std::string queueDir_;
};