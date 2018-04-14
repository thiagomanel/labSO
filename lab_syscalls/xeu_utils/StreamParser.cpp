#include "ParsingState.h"
#include "StreamParser.h"

#include <stdexcept>
#include <string>
#include <iostream>

namespace xeu_utils {

StreamParser::StreamParser(const std::string& line_prefix, bool handle_errors)
  : line_prefix_(line_prefix), handle_errors_(handle_errors) {}

ParsingState StreamParser::parse(
  std::string& unparsed_input,
  std::istream& input,
  std::ostream& output
) const {
  ParsingState p;
  std::string s;
  unparsed_input = "";
  while (!p.completed()) {
    std::getline(input, s);
    s += '\n';
    unparsed_input += s;
    try {
      p.parse_next(s);
    } catch (std::runtime_error& e) {
      if (handle_errors_) {
        output << "xeu: " << e.what() << std::endl;
        return p;
      } else {
        throw;
      }
    }
    if (!p.completed()) {
      output << line_prefix_;
    }
  }
  return p;
}

ParsingState StreamParser::parse(
  std::istream& input,
  std::ostream& output
) const {
  std::string tmp;
  return parse(tmp, input, output);
}

};