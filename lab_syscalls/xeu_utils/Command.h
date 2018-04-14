#pragma once

#include <ostream>
#include <vector>
#include <string>

namespace xeu_utils {

struct Command {
  Command();
  Command(const Command& other);
  Command& operator=(const Command& rhs);
  ~Command();

  /**
   * NOTE: this is useful for using in exec*.
   * Returns the filename in the command (i.e. the first arg == argv[0]), or a
   * pointer to an empty string if the command has no args.
   */
  const char* filename() const;

  /**
   * NOTE: this is useful for using in exec*.
   * Returns a constant pointer to the args in the format required by some of
   * exec variations (possibly the one you will choose to use).
   */
  char* const* argv() const;

  /**
   * Returns the file/command name (like filename() above, but in std::string).
   */
  std::string name() const;

  /**
   * Returns a list of all the args as a vector of strings.
   */
  const std::vector<std::string>& args() const;

  /**
   * Returns a representation of this command that could be run in our xeu
   * and would produce the exact same command (i.e. same filename, same args).
   */
  std::string repr() const;
  operator std::string() const;

  /**
   * Outputs command.repr() to the stream.
   */
  friend std::ostream& operator<<(std::ostream& os, const Command& command);

  /**
   * Pushes a new arg to the arg list of the command.
   */
  void add_arg(const std::string& arg);

  /**
   * Similar to repr() above, but for a vector of commands. It just returns:
   *   commands[0].repr() + " | " + commands[1].repr() + ...
   * In other words, a string with each command separated by a pipe character.
   */
  static std::string repr(const std::vector<Command>& commands);

  /**
   * Escapes an arg and embeds it in double quotes.
   */
  static std::string escape_arg(const std::string& unescaped_arg);

  /**
   * Escapes an arg and embeds it in double quotes if needed. If escaping is
   * not necessary, just returns the arg unmodified. See requires_escaping().
   */
  static std::string escape_arg_if_needed(const std::string& unescaped_arg);

  /**
   * Returns whether a character inside an arg would require escaping or not.
   */
  static bool requires_escaping(char c);

 private:
  std::vector<char*> argv_; // stores the data in C string format (for exec*)
  std::vector<std::string> args_; // stores the data as C++ strings
};

};
