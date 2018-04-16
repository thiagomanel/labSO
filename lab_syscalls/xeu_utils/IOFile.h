#pragma once

#include <string>

namespace xeu_utils {

struct IOFile {
  static const int INVALID_FD = -1;

  IOFile();
  IOFile(int fd, bool input, std::string path);

  /**
   * The file descriptor to use for the file.
   */
  int fd() const;

  /**
   * Should we read from (input) or write to (output) this file?
   */
  bool is_input() const;
  bool is_output() const;

  /**
   * Returns the path of the file to use.
   */
  std::string path() const;

  /**
   * Displays a representation of this IOFile e.g. 2>/path/a.txt
   */
  std::string repr() const;

  /**
   * Returns whether this has an fd or not (i.e. fd != INVALID_FD).
   */
  bool has_fd() const;

  /**
   * Create a new IOFile with some parameter changed.
   */
  IOFile with_fd(int fd) const;
  IOFile with_input(bool input) const;
  IOFile with_path(std::string path) const;

 private:
  bool input_;
  int fd_;
  std::string path_;
};

};