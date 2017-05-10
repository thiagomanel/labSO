#include "Command.h"

#include <sstream>
#include <string>
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

const char* Command::filename() {
  return argv_[0];
}

char* const* Command::argv() {
  return &argv_[0];
}

const std::vector<std::string>& Command::args() {
  return args_;
}

void Command::add_arg(const std::string& arg) {
  args_.push_back(arg);
  
  char* n = new char[arg.length()+1];
  memcpy(n, arg.c_str(), arg.length());
  n[arg.length()] = 0;
  
  argv_.back() = n;
  argv_.push_back(0);
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

};
