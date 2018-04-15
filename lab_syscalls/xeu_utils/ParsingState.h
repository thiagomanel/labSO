#pragma once

#include "Command.h"
#include "IOFile.h"

#include <string>
#include <vector>

namespace xeu_utils {

struct ParsingState {
  ParsingState();

  /**
   * Returns whether the parsing is in a final ("completed") state or not.
   */
  bool completed() const;

  /**
   * Returns whether an user/syntax error occurred during parsing or not.
   * Errors that we know how to handle do not set this to true; those include:
   * - Receiving NUL character: we just ignore it
   * - Receiving more input after reaching a final state: we already have a nice
   *   final state, so no need to set this flag.
   * Errors that currently set this flag to true are:
   * - Receiving a pipe symbol (|) when we have 0 args for the current command
   */
  bool error() const;

  /**
   * Returns a list of all the commands fully parsed. Note that each command is
   * separated by a pipe character '|' in the original input.
   * e.g. "ps aux | grep hh_server | wc -l\n" results in three commands:
   *   commands()[0] = ps aux
   *   commands()[1] = grep hh_server
   *   comamnds()[2] = wc -l
   */
  const std::vector<Command> commands() const;

  /**
   * Produces a string with a dump of the entire state. You can then print it:
   * std::cout << p.dump(); // where p is an instance of this ParsingState
   */
  std::string dump() const;

  /**
   * Calls parse_next(char) for each character in s, until either we call it
   * for all character in s or we reach a final ("completed") state.
   * Returns how many characters were parsed (may be less than s.length() if we
   * reached a final state before iterating over all characters in s).
   */
  int parse_next(const std::string& s);

  /**
   * Advances the state. This is a state machine: we are on a state S(str) and
   * receive c, so we must advance to state S(str+c).
   */
  void parse_next(char c);

 private:
  void complete_arg();
  bool complete_command(bool in_final_state=true);

  bool completed_;
  bool backslash_;
  bool error_;
  char quotes_;
  IOFile io_;
  std::string current_arg_;
  Command current_command_;
  std::vector<Command> parsed_commands_;
};

};