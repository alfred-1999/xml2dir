#include "xml2dir/FileQueue.hpp"
#include <filesystem>

FileQueue::FileQueue(std::string queueDir) : queueDir_(std::move(queueDir)) {}

std::vector<std::string> FileQueue::pending() const {
    std::vector<std::string> files;
    if (!fs::exists(queueDir_)) return files;
    for (const auto& entry : fs::directory_iterator(queueDir_)) {
        if (entry.is_regular_file() && entry.path().extension() == ".xml") {
            files.push_back(entry.path().string());
        }
    }
    return files;
}