#pragma once    // Prevent this header from being loaded twice
#include <string>
#include <fstream>
#include <mutex> // For thread-safe logging //It provides tools to lock resources so only one thread can access them at a time

enum class LogLevel { INFO, WARNING, ERROR };

class Logger {
    public:
        static Logger& instance(); // Singleton instance
        void init(const std::string& logFilePath);
        void log(LogLevel level, const std::string& message);
    private:
        Logger() = default;     // Private constructor for singleton
        std::ofstream logfile;  // The actual file handler
        std::mutex logMutex;    // Mutex for thread-safe logging
                                // Prevents threads from overlapping writes
        static std::string levelToString(LogLevel level);   // Function to convert LogLevel enum to string
        static std::string timestamp(); // Function to get the current timestamp
};


// Macros for easier logging
// sysntax:
//  #define Macro_Name replacement_text/value1
//  #define value1  final_value
//  #define Macro_Name(parameters) replacement_text
//  #define
#define LOG_INFO(message) Logger::instance().log(LogLevel::INFO, message)
#define LOG_WARNING(message) Logger::instance().log(LogLevel::WARNING, message)
#define LOG_ERROR(message) Logger::instance().log(LogLevel::ERROR, message)