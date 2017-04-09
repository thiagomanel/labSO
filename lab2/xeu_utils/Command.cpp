#include "Command.h"

#include <sstream>
#include <string>
#include <vector>

namespace xeu_utils {

Command::Command() {
  argv_.push_back(0);
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
  argv_.back() = const_cast<char*>(args_.back().c_str());
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