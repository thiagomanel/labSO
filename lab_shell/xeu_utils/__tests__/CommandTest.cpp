#include "__lib__/catch.hpp"
#include "../Command.h"

#include <cstring>
#include <iostream>

using namespace xeu_utils;

TEST_CASE("[Command] empty constructor", "[Command]") {
  Command empty;

  // make sure everything starts empty
  REQUIRE(empty.args().size() == 0);
  REQUIRE(empty.io().size() == 0);
}

TEST_CASE("[Command] add_arg() and args()", "[Command]") {
  Command cmd;

  // single arg
  cmd.add_arg("arg1");
  REQUIRE(cmd.args().size() == 1);
  REQUIRE(cmd.args()[0] == "arg1");

  // multi arg
  cmd.add_arg("arg2");
  REQUIRE(cmd.args().size() == 2);
  REQUIRE(cmd.args()[0] == "arg1");
  REQUIRE(cmd.args()[1] == "arg2");
}

TEST_CASE("[Command] name()", "[Command]") {
  Command cmd;

  // when no args are provided, should return emoty string
  REQUIRE(cmd.name() == "");

  // return first arg
  cmd.add_arg("arg1");
  REQUIRE(cmd.name() == "arg1");

  // still should return first arg
  cmd.add_arg("arg2");
  REQUIRE(cmd.name() == "arg1");
}

TEST_CASE("[Command] argv()", "[Command]") {
  Command cmd;

  // argv should never be NULL, only its first element should if args is empty
  // i.e. it has (args().size() + 1) elements, where the last is always NULL
  REQUIRE(cmd.argv() != NULL);
  REQUIRE(*cmd.argv() == NULL);

  // the first arg should be what was added, but still should end in a NULL arg
  cmd.add_arg("arg1");
  REQUIRE(cmd.argv()[0] != NULL);
  REQUIRE(cmd.argv()[1] == NULL);
  REQUIRE(strcmp(cmd.argv()[0], "arg1") == 0);

  // add one more, make sure all are correct and last is NULL
  cmd.add_arg("arg2");
  REQUIRE(cmd.argv()[0] != NULL);
  REQUIRE(cmd.argv()[1] != NULL);
  REQUIRE(cmd.argv()[2] == NULL);
  REQUIRE(strcmp(cmd.argv()[0], "arg1") == 0);
  REQUIRE(strcmp(cmd.argv()[1], "arg2") == 0);
}

TEST_CASE("[Command] filename()", "[Command]") {
  Command cmd;

  // filename should never return NULL; if it has no args, return empty
  REQUIRE(strcmp(cmd.filename(), "") == 0);

  // return first arg
  cmd.add_arg("arg1");
  REQUIRE(strcmp(cmd.filename(), "arg1") == 0);

  // still should return first arg
  cmd.add_arg("arg2");
  REQUIRE(strcmp(cmd.filename(), "arg1") == 0);
}

TEST_CASE("[Command] add_io() and io()", "[Command]") {
  Command cmd;
  IOFile io(7, true, "path");
  IOFile io2(8, false, "out");

  // a new command should have no io
  REQUIRE(cmd.io().size() == 0);

  // simple case: should add io when add_io is called
  cmd.add_io(io);
  REQUIRE(cmd.io().size() == 1);
  REQUIRE(cmd.io()[0].repr() == io.repr());

  // should allow identical io
  cmd.add_io(io);
  REQUIRE(cmd.io().size() == 2);
  REQUIRE(cmd.io()[0].repr() == io.repr());
  REQUIRE(cmd.io()[1].repr() == io.repr());

  // should obviously allow different io
  cmd.add_io(io2);
  REQUIRE(cmd.io().size() == 3);
  REQUIRE(cmd.io()[1].repr() == io.repr());
  REQUIRE(cmd.io()[2].repr() == io2.repr());
}

TEST_CASE("[Command] repr()", "[Command]") {
  Command cmd;

  // a new command should have an empty representation
  REQUIRE(cmd.repr() == "");
  REQUIRE(cmd.repr(false) == "");

  // both repr() and repr(false) should return the args separated by space
  cmd.add_arg("arg1");
  cmd.add_arg("arg2");
  REQUIRE(cmd.repr() == "arg1 arg2");
  REQUIRE(cmd.repr(false) == "arg1 arg2");

  // should print io for repr() and not print for repr(false)
  cmd.add_io(IOFile(2, false, "out"));
  REQUIRE(cmd.repr() == "arg1 arg2 2>out");
  REQUIRE(cmd.repr(false) == "arg1 arg2");

  // should include all io's, even if identical
  cmd.add_io(IOFile(2, false, "out"));
  REQUIRE(cmd.repr() == "arg1 arg2 2>out 2>out");
  REQUIRE(cmd.repr(false) == "arg1 arg2");

  // should return input as well as output
  cmd.add_io(IOFile(7, true, "in"));
  REQUIRE(cmd.repr() == "arg1 arg2 2>out 2>out 7<in");
  REQUIRE(cmd.repr(false) == "arg1 arg2");
}

TEST_CASE("[Command] operator=(Command) and Command(Command)", "[Command]") {
  Command empty;
  Command cmd;

  cmd.add_arg("a1");
  cmd.add_arg("a2");
  cmd.add_io(IOFile(3, false, "path"));
  REQUIRE(cmd.repr() != empty.repr());

  // operator= should create a command with the exact same repr()
  empty = cmd;
  REQUIRE(cmd.repr() == empty.repr());

  // constructor(Command) should create a command with the exact same repr()
  REQUIRE(cmd.repr() == Command(cmd).repr());
}

TEST_CASE("[Command] repr() escaping", "[Command]") {
  Command cmd;

  cmd.add_arg("noescaping");
  cmd.add_arg("needs escaping");
  cmd.add_arg("a b");
  cmd.add_arg("noescaping");

  // escaping should happen if and only if necessary
  REQUIRE(cmd.repr() == "noescaping \"needs escaping\" \"a b\" noescaping");
}