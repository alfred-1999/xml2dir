#pragma once
#include "xml2dir/Config.hpp"
#include <atomic>

class Service {
public:
    explicit Service(Config config);
    void run();   // blocks until stop() is called
    void stop();  // signal the loop to exit

private:
    Config config_;
    std::atomic<bool> running_{false};
};