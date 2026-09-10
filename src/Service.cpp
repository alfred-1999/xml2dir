#include "xml2dir/Service.hpp"
#include "xml2dir/Logger.hpp"
#include "xml2dir/FileQueue.hpp"
#include "xml2dir/XmlRouter.hpp"
#include <chrono>
#include <thread>

Service::Service(Config config) : config_(std::move(config)) {}

void Service::stop() {
    running_ = false;
    LOG_INFO("Stop requested.");
}

void Service::run() {
    running_ = true;
    LOG_INFO("Service started. Watching: " + config_.queueDir);

    FileQueue queue(config_.queueDir);
    XmlRouter router(config_.outputRoot);

    while (running_) {
        for (const auto& file : queue.pending()) {
            router.route(file);
        }
        std::this_thread::sleep_for(
            std::chrono::milliseconds(config_.pollIntervalMs));
    }

    LOG_INFO("Service stopped.");
}