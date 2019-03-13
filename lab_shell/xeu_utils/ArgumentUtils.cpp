#include "ArgumentUtils.h"

#include <string>
#include <sstream>

namespace xeu_utils {

std::string ArgumentUtils::escape(const std::string& unescaped_arg) {
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

std::string ArgumentUtils::escape_if_needed(
  const std::string& unescaped_arg
) {
  for (size_t i = 0; i < unescaped_arg.length(); i++) {
    if (requires_escaping(unescaped_arg[i])) {
      return escape(unescaped_arg);
    }
  }
  return unescaped_arg;
}

bool ArgumentUtils::requires_escaping(char c) {
  return c <= 32 || c == '\'' || c == '"' || c == '\\' || c == '|' ||
    c == '<' || c == '>';
}

};