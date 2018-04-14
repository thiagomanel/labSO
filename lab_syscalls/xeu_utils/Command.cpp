#include "Command.h"

#include <sstream>
#include <string>
#include <cstring>
#include <vector>

namespace xeu_utils {

Command::Command() {
  argv_.push_back(0);
}

Command::Command(const Command& other) {
    argv_.push_back(0);
    for (int i = 0; i < other.args_.size(); i++) {
        add_arg(other.args_[i]);
    }
}

Command& Command::operator=(const Command& other) {
    args_.clear();
    argv_.clear();
    argv_.push_back(0);
    for (int i = 0; i < other.args_.size(); i++) {
        add_arg(other.args_[i]);
    }
    return *this;
}

Command::~Command() {
    for (int i = 0; i < argv_.size()-1; i++) {
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

const std::vector<std::string>& Command::args() const {
  return args_;
}

std::string Command::repr() const {
  if (args_.empty()) {
    return "";
  }
  std::stringstream ss;
  ss << escape_arg_if_needed(args_[0]);
  for (int i = 1; i < args_.size(); i++) {
    ss << " " << escape_arg_if_needed(args_[i]);
  }
  return ss.str();
}

void Command::add_arg(const std::string& arg) {
  args_.push_back(arg);

  char* n = new char[arg.length()+1];
  memcpy(n, arg.c_str(), arg.length());
  n[arg.length()] = 0;

  argv_.back() = n;
  argv_.push_back(0);
}

std::string Command::repr(const std::vector<Command>& commands) {
  if (commands.empty()) {
    return "";
  }
  std::stringstream ss;
  for (size_t i = 0; i < commands.size(); i++) {
    if (i != 0) {
      ss << " | "; // pipe symbol between two commands
    }
    ss << commands[i].repr();
  }
  return ss.str();
}

std::string Command::escape_arg(const std::string& unescaped_arg) {
  std::stringstream ss;
  ss << '"';
  for (size_t i = 0; i < unescaped_arg.length(); i++) {
    char c = unescaped_arg[i];
    if (c == '"' || c == '\\') {
      ss << '\\';
    }
    ss << c;
  }
  ss << '"';
  return ss.str();
}

std::string Command::escape_arg_if_needed(const std::string& unescaped_arg) {
  for (size_t i = 0; i < unescaped_arg.length(); i++) {
    if (requires_escaping(unescaped_arg[i])) {
      return escape_arg(unescaped_arg);
    }
  }
  return unescaped_arg;
}

bool Command::requires_escaping(char c) {
  return c <= 32 || c == '\'' || c == '"' || c == '|' || c == '\\';
}

};
