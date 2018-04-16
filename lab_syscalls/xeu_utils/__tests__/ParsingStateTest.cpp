// This is still missing a lot of corner and special cases
// And missing any cases where the parsing should fail...

#include "__lib__/catch.hpp"
#include "../ParsingState.h"
#include <string>

using namespace xeu_utils;

// Notice that repr() doesn't always produce the exact same text that was used
// to produce the given state. In these cases, specify the output as well.
#define REQUIRE_PRODUCES(input, ...) \
  do { \
    const std::string& repr = std::string(#__VA_ARGS__) == std::string("") \
      ? std::string(input) \
      : std::string(__VA_ARGS__); \
    ParsingState p; \
    p.parse_next(std::string(input) + "\n"); \
    REQUIRE(p.completed() == true); \
    REQUIRE(p.error() == false); \
    REQUIRE(Command::repr(p.commands()) == repr); \
  } while (0)

TEST_CASE("[ParsingState] empty constructor", "[ParsingState]") {
  ParsingState p;

  // state shouldn't start broken (completed or with errors)
  REQUIRE(p.completed() == false);
  REQUIRE(p.error() == false);

  // state shouldn't start with any commands
  REQUIRE(p.commands().size() == 0);
}

TEST_CASE("[ParsingState] parse_next() simple", "[ParsingState]") {
  {
    ParsingState p;

    // make sure it doesn't complete before '\n' is given
    REQUIRE(p.parse_next("ps aux") == std::string("ps aux").length());
    REQUIRE(p.completed() == false);
    REQUIRE(p.error() == false);

    // make sure giving '\n' now is enough to complete
    p.parse_next('\n');
    REQUIRE(p.completed() == true);
  }

  {
    ParsingState p;

    // should complete and produce one command
    REQUIRE(p.parse_next("ps aux\n") == std::string("ps aux\n").length());
    REQUIRE(p.completed() == true);
    REQUIRE(p.commands().size() == 1);
    REQUIRE(p.commands()[0].repr() == "ps aux");
  }
}

TEST_CASE("[ParsingState] parse_next() with special quotes", "[ParsingState]") {
  // just quotes
  REQUIRE_PRODUCES("\"ps aux\"");

  // backslash and special quotes with random letters
  REQUIRE_PRODUCES("\" a\\\\n\\\"\\\\ \"");

  // newline
  REQUIRE_PRODUCES("\"\n\"");
  REQUIRE_PRODUCES("\"line1\nline2\"");

  // single quotes
  REQUIRE_PRODUCES("\"'\"");

  // pipe, and io redirection
  REQUIRE_PRODUCES("\"ps aux | grep xeu <in >out\"");

  // quotes in middle of arg
  REQUIRE_PRODUCES("a\"b\"c\"\"d", "abcd");

  // FIXME: this passes, it shouldn't. Should produce "\"\"".
  REQUIRE_PRODUCES("\"\"", "");
}

TEST_CASE("[ParsingState] parse_next() with single quotes", "[ParsingState]") {
  // just quotes
  REQUIRE_PRODUCES("'ps aux'", "\"ps aux\"");

  // backslash and special quotes with random letters
  // there is no escaping inside single quotes, so '\' and "\\" are the same
  // that's why it looks like we are doubling the number of backslashes
  REQUIRE_PRODUCES("' a\\\\n\\\"\\\\ '", "\" a\\\\\\\\n\\\\\\\"\\\\\\\\ \"");

  // newline
  REQUIRE_PRODUCES("'\n'", "\"\n\"");
  REQUIRE_PRODUCES("'line1\nline2'", "\"line1\nline2\"");

  // single quotes
  // '\' would result in "\\" while '\'' would wait for more input, because
  // \ doesn't escape ' inside ', so there is one ' missing: '\'''.
  // In other words, you can't include ' inside '
  REQUIRE_PRODUCES("'\\'''", "\"\\\\\"");
  REQUIRE_PRODUCES("'\\'\\'", "\"\\\\'\"");

  // pipe, and io redirection
  REQUIRE_PRODUCES("'ps aux | grep xeu <i >o'", "\"ps aux | grep xeu <i >o\"");

  // // quotes in middle of arg
  // REQUIRE_PRODUCES("a\"b\"c\"\"d", "abcd");

  // FIXME: this passes, it shouldn't. Should produce "\"\"".
  REQUIRE_PRODUCES("''''", "");
}

TEST_CASE("[ParsingState] parse_next() simple pipe", "[ParsingState]") {
  // basic pipe
  REQUIRE_PRODUCES("ps aux | grep xeu");

  // multi pipe
  REQUIRE_PRODUCES("ps aux | grep xeu | wc -l");

  // no unnecessary spaces
  REQUIRE_PRODUCES("ps aux|grep xeu|wc -l", "ps aux | grep xeu | wc -l");
}

TEST_CASE("[ParsingState] parse_next() simple io", "[ParsingState]") {
  // simple cases
  REQUIRE_PRODUCES("ps aux <in");
  REQUIRE_PRODUCES("ps aux >out");
  REQUIRE_PRODUCES("ps aux 2>err");
  REQUIRE_PRODUCES("ps aux <in >out");
  REQUIRE_PRODUCES("ps aux <in >out 2>err");

  // weird cases
  REQUIRE_PRODUCES("ps aux <in <in <in2 >out >out 2>err");
  REQUIRE_PRODUCES("ps aux 22299>out");
  REQUIRE_PRODUCES("ps aux 0>out");
  REQUIRE_PRODUCES("ps aux 1<in");

  // special cases
  REQUIRE_PRODUCES("ps aux<in>out", "ps aux <in >out");
  REQUIRE_PRODUCES("ps aux>out<in", "ps aux >out <in");
  REQUIRE_PRODUCES("ps aux3<in>out", "ps aux3 <in >out");
  REQUIRE_PRODUCES("ps 3<in>out", "ps 3<in >out");
  REQUIRE_PRODUCES("ps aux 2<3<4>5>6", "ps aux 2<3 <4 >5 >6");
}

TEST_CASE("[ParsingState] parse_next() pipe + io", "[ParsingState]") {
  // basic cases
  REQUIRE_PRODUCES("ps aux <in | grep xeu");
  REQUIRE_PRODUCES("ps aux <in | grep xeu >out");
  REQUIRE_PRODUCES("ps aux <in >out | grep xeu 2>err");

  // without useless separators
  REQUIRE_PRODUCES(
    "ps aux<in|grep xeu>out|wc -l",
    "ps aux <in | grep xeu >out | wc -l"
  );
}

#undef REQUIRE_PRODUCES