#include "ArgumentUtils.h"
#include "Command.h"
#include "IOFile.h"

#include <sstream>
#include <string>
#include <cstring>
#include <vector>

namespace xeu_utils {

Command::Command() {
  argv_.push_back(0);
}

Command::Command(const Command& other) {
  operator=(other);
}

Command& Command::operator=(const Command& other) {
  args_.clear();
  argv_.clear();
  io_.clear();
  argv_.push_back(0);
  for (size_t i = 0; i < other.args_.size(); i++) {
    add_arg(other.args_[i]);
  }
  for (size_t i = 0; i < other.io_.size(); i++) {
    add_io(other.io_[i]);
  }
  return *this;
}

Command::~Command() {
  for (size_t i = 0; i < argv_.size() - 1; i++) {
    delete[] argv_[i];
  }
  argv_.clear();
}

const char* Command::filename() const {
  static char NIL = 0;
  return args_.empty() ? &NIL : argv_[0];
}

char* const* Command::argv() const {
  return &argv_[0];
}

std::string Command::name() const {
  return args_.empty() ? "" : args_[0];
}

const std::vector<std::string>& Command::args() const {
  return args_;
}

const std::vector<IOFile>& Command::io() const {
  return io_;
}

std::string Command::repr(bool show_io) const {
  if (args_.empty()) {
    return "";
  }
  std::stringstream ss;
  ss << ArgumentUtils::escape_if_needed(args_[0]);
  for (size_t i = 1; i < args_.size(); i++) {
    ss << " " << ArgumentUtils::escape_if_needed(args_[i]);
  }
  if (show_io) {
    for (size_t i = 0; i < io_.size(); i++) {
      ss << " " << io_[i].repr();
    }
  }
  return ss.str();
}

Command::operator std::string() const {
  return repr();
}

std::ostream& operator<<(std::ostream& os, const Command& command) {
  return os << command.repr();
}

void Command::add_arg(const std::string& arg) {
  argv_.back() = new char[arg.length() + 1];
  memcpy(argv_.back(), arg.c_str(), arg.length() + 1);
  argv_.push_back(0);
  args_.push_back(arg);
}

void Command::add_io(const IOFile& io) {
  io_.push_back(io);
}

std::string Command::repr(const std::vector<Command>& commands, bool show_io) {
  if (commands.empty()) {
    return "";
  }
  std::stringstream ss;
  for (size_t i = 0; i < commands.size(); i++) {
    if (i != 0) {
      ss << " | "; // pipe symbol between two commands
    }
    ss << commands[i].repr(show_io);
  }
  return ss.str();
}

};
