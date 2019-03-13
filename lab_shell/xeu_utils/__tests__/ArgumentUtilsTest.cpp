#include "__lib__/catch.hpp"
#include "../ArgumentUtils.h"

using namespace xeu_utils;

TEST_CASE("[ArgumentUtils] escape()", "[ArgumentUtils]") {
  REQUIRE(ArgumentUtils::escape("someArg") == "\"someArg\"");

  // when escaping, if '\\' is encountered, just double it
  REQUIRE(ArgumentUtils::escape_if_needed("a\\ b") == "\"a\\\\ b\"");
  REQUIRE(ArgumentUtils::escape_if_needed("a \\b") == "\"a \\\\b\"");
}

TEST_CASE("[ArgumentUtils] escape_if_needed()", "[ArgumentUtils]") {
  REQUIRE(ArgumentUtils::escape_if_needed("someArg") == "someArg");

  // escape separators/delimiters
  REQUIRE(ArgumentUtils::escape_if_needed("a b") == "\"a b\"");

  // escape backslash and quotes
  REQUIRE(ArgumentUtils::escape_if_needed("\\") == "\"\\\\\"");
  REQUIRE(ArgumentUtils::escape_if_needed("\"") == "\"\\\"\"");
  REQUIRE(ArgumentUtils::escape_if_needed("'") == "\"'\"");

  // escape reserved characters (|, <, >)
  REQUIRE(ArgumentUtils::escape_if_needed("<") == "\"<\"");
  REQUIRE(ArgumentUtils::escape_if_needed(">") == "\">\"");
  REQUIRE(ArgumentUtils::escape_if_needed("|") == "\"|\"");
}
