#include <xml2dir/Logger.hpp>
#include <iostream>     // For console output
#include <chrono>       // For timestamping
#include <iomanip>      // For formatting timestamps
#include <ctime>        // For converting time to local time
#include <sstream>      // For string stream operations

// Singleton instance of Logger
Logger& Logger::instance() {
    static Logger instance; // Guaranteed to be destroyed and instantiated on first use
    return instance;
}
// Initialize the logger with a file path
void Logger::init(const std::string& logFilePath) {
    std::lock_guard<std::mutex> lock(logMutex); // Ensure thread-safe initialization
    logfile.open(logFilePath, std::ios::app);
}


// Log a message with a specific log level
std::string Logger::timestamp() {
    auto now = std::chrono::system_clock::now();    // Get the current time point
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);   // Convert to time_t for localtime_r
    std::tm local_tm{};                // Initialize a tm structure to hold local time
    localtime_r(&now_time, &local_tm); // Thread-safe conversion to local time
    std::ostringstream oss;             // Create a string stream to format the timestamp
    oss << std::put_time(&local_tm, "%Y-%m-%d_%H-%M-%S"); // Format the timestamp as "YYYY-MM-DD_HH-MM-SS"
    
    return oss.str(); // Return the formatted timestamp as a string
}

// Convert LogLevel enum to string representation
std::string Logger::levelToString(LogLevel level) {
    switch (level) {
        case LogLevel::INFO: return "INFO";
        case LogLevel::WARNING: return "WARNING";
        case LogLevel::ERROR: return "ERROR";
        default: return "UNKNOWN";
    }
    return "UNKNOWN"; // Fallback in case of an unrecognized log level
}

void Logger::log(LogLevel level, const std::string& message) {
    std::lock_guard<std::mutex> lock(logMutex);
    std::string line = "[" + timestamp() + "] [" + levelToString(level) + "] " + message;
    std::cout << line << std::endl;
    if (logfile.is_open()) {
        logfile << line << std::endl;
        logfile.flush();
    }
}