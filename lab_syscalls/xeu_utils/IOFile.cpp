#include "IOFile.h"

#include "ArgumentUtils.h"

#include <sstream>
#include <string>

namespace xeu_utils {

IOFile::IOFile(): fd_(INVALID_FD), input_(false) {}
IOFile::IOFile(int fd, bool input, std::string path)
  : fd_(fd), input_(input), path_(path) {}

int IOFile::fd() const {
  return fd_;
}

bool IOFile::is_input() const {
  return input_;
}

bool IOFile::is_output() const {
  return !input_;
}

std::string IOFile::path() const {
  return path_;
}

std::string IOFile::repr() const {
  std::stringstream ss;
  // show fd in all cases but "0<" and "1>" (should be just "<" and ">")
  if ((fd_ && input_) || (fd_ != 1 && !input_)) {
    ss << fd_;
  }
  ss << (input_ ? '<' : '>') << ArgumentUtils::escape_if_needed(path_);
  return ss.str();
}

bool IOFile::has_fd() const {
  return fd_ != INVALID_FD;
}

IOFile IOFile::with_fd(int fd) const {
  return IOFile(fd, input_, path_);
}

IOFile IOFile::with_input(bool input) const {
  return IOFile(fd_, input, path_);
}

IOFile IOFile::with_path(std::string path) const {
  return IOFile(fd_, input_, path);
}

};