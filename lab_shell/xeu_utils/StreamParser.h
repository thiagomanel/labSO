#pragma once

#include "ParsingState.h"

#include <string>
#include <iostream>

namespace xeu_utils {

struct StreamParser {
  StreamParser(
    const std::string& line_prefix="> ",
    bool handle_errors=true
  );

  /**
   * Parses the input until a final state is reached. Since a command may be
   * split into multiple lines (by ending a line with \ or by using quotes),
   * this method prints a line_prefix_ string to output for each extra new line.
   */
  ParsingState parse(
    std::istream& input=std::cin,
    std::ostream& output=std::cout
  ) const;

  /**
   * Similar to parse(istream&, ostream&), but copies the input string to
   * unparsed_input, so you can use it later if you need.
   */
  ParsingState parse(
    std::string& unparsed_input,
    std::istream& input=std::cin,
    std::ostream& output=std::cout
  ) const;

 private:
  std::string line_prefix_;
  bool handle_errors_;
};

};