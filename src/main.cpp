#include "xml2dir/Service.hpp"
#include "xml2dir/Config.hpp"
#include "xml2dir/Logger.hpp"
#include <csignal>
#include <iostream>

static Service* g_service = nullptr;

static void handleSignal(int) {
    if (g_service) g_service->stop();
}

int main(int argc, char** argv) {
    std::string configPath = "config/xml2dir.conf";
    if (argc > 1) configPath = argv[1];

    Config config;
    if (!Config::load(configPath, config)) {
        std::cerr << "Failed to load config: " << configPath << std::endl;
        return 1;
    }

    Logger::instance().init(config.logFile);
    LOG_INFO("Loaded config from " + configPath);

    Service service(config);
    g_service = &service;

    std::signal(SIGINT, handleSignal);
    std::signal(SIGTERM, handleSignal);

    service.run();
    return 0;
}