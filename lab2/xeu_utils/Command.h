#pragma once

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
  const char* filename();

  /**
   * NOTE: this is useful for using in exec*.
   * Returns a constant pointer to the args in the format required by some of
   * exec variations (possibly the one you will choose to use).
   */
  char* const* argv();

  /**
   * Returns a list of all the args as a vector of strings.
   */
  const std::vector<std::string>& args();

  /**
   * Pushes a new arg to the arg list of the command.
   */
  void add_arg(const std::string& arg);

  /**
   * Escapes an arg and embeds it in double quotes.
   */
  static std::string escape_arg(const std::string& unescaped_arg);

 private:
  std::vector<char*> argv_; // stores pointers to the data (for use in exec*)
  std::vector<std::string> args_; // stores the data
};

};
