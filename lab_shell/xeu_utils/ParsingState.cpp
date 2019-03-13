#include "Command.h"
#include "IOFile.h"
#include "ParsingState.h"

#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace xeu_utils {

ParsingState::ParsingState()
  : completed_(0), backslash_(0), quotes_(0), error_(0) {}

bool ParsingState::error() const {
  return error_;
}

bool ParsingState::completed() const {
  return completed_;
}

const std::vector<Command> ParsingState::commands() const {
  return parsed_commands_;
}

std::string ParsingState::dump() const {
  std::stringstream ss;

  // general
  {
    ss
      << "ParsingState [addr=" << this << "]" << std::endl
      << "> completed_: " << completed_ << std::endl
      << "> backslash_: " << backslash_ << std::endl
      << "> error_: " << error_ << std::endl
      << "> quotes_: " << quotes_ << " (" << (int) quotes_ << ")" << std::endl
      << "> current_arg_: " << current_arg_ << std::endl;
  }
  // current_command_
  {
    const std::vector<std::string>& args = current_command_.args();
    ss << "> current_command_.args(): " << args.size() << std::endl;
    for (size_t i = 0; i < args.size(); i++) {
      ss << ">> [" << i << "] " << args[i] << std::endl;
    }
  }
  // parsed_commands_
  {
    ss << "> parsed_commands_: " << parsed_commands_.size() << std::endl;
    for (size_t i = 0; i < parsed_commands_.size(); i++) {
      const std::vector<std::string>& args = parsed_commands_[i].args();
      ss << ">> [" << i << "].args(): " << args.size() << std::endl;
      for (size_t j = 0; j < args.size(); j++) {
        ss << ">>> [" << j << "] " << args[j] << std::endl;
      }
    }
  }
  // io_
  {
    ss
      << "> io_: fd=" << io_.fd()
      << " path=" << io_.path()
      << " input=" << io_.is_input()
      << std::endl;
  }
  return ss.str();
}

int ParsingState::parse_next(const std::string& s) {
  for (size_t i = 0; i < s.length(); i++) {
    if (completed_) {
      return i;
    }
    parse_next(s[i]);
  }
  return s.length();
}

void ParsingState::parse_next(char c) {
  const char SIMPLE_QUOTES = '\'';
  const char SPECIAL_QUOTES = '"';
  const char NO_QUOTES = '\0';

  if (!c) {
    throw std::runtime_error("Can't parse a NUL character.");
  } else if (completed_) {
    throw std::runtime_error("This is already a final state. See completed().");
  }

  switch (c) {
   case '\n':
    if (backslash_) {
      backslash_ = false;
    } else if (quotes_ != NO_QUOTES) {
      current_arg_ += c;
    } else {
      complete_command(true /* set this as a final state */);
    }
    return;

   case '\\':
    if (backslash_ || quotes_ == SIMPLE_QUOTES) {
      current_arg_ += c;
      backslash_ = false;
    } else {
      backslash_ = true;
    }
    return;

   case SPECIAL_QUOTES:
   case SIMPLE_QUOTES:
    // [special case] (\' inside "") is kept exactly as \'
    if (backslash_ && quotes_ == SPECIAL_QUOTES && c == SIMPLE_QUOTES) {
      current_arg_ += '\\';
    }
    // (\') or (\") or (' inside ") or (" inside ')
    if (backslash_ || (quotes_ != NO_QUOTES && c != quotes_)) {
      current_arg_ += c;
    } else {
      quotes_ = (c == quotes_ ? 0 : c);
    }
    backslash_ = false;
    return;

   case '>':
   case '<':
    if (backslash_ || quotes_ != NO_QUOTES) {
      break; // fallthrough, not an io redirection
    }
    if (io_.has_fd()) {
      complete_arg();
      if (io_.has_fd()) {
        error_ = true;
        throw std::runtime_error(
          "syntax error: << and >> are not supported.");
      }
    }
    // get fd and complete arg
    {
      int fd = IOFile::INVALID_FD;
      if (current_arg_.length() > 0) {
        std::stringstream(current_arg_) >> fd;
        std::stringstream ss; ss << fd;
        if (fd == IOFile::INVALID_FD || ss.str() != current_arg_) {
          // Not a valid non-negative integer, so treat it as an arg, not an fd
          complete_arg();
          fd = IOFile::INVALID_FD;
        } else {
          current_arg_ = "";
        }
      }
      fd = (fd == IOFile::INVALID_FD) ? (c == '>') : fd; // '<' = 0, '>' = 1
      // set io
      io_ = io_.with_fd(fd).with_input(c == '<');
    }
    return;

   case '|':
    // check if this is a pipe
    if (!backslash_ && quotes_ == NO_QUOTES) {
      if (!complete_command(false /* do not set this as a final state */)) {
        // something like: "some_command | | other_command" happened
        // even "cmd1 || cmd2" causes this, since we don't understand "||" as
        // the OR operator, but instead we process it as two pipe symbols
        error_ = true;
        throw std::runtime_error("syntax error near unexpected token `|'");
      }
      return;
    }
    break; // fallthrough, this is not a pipe!
  }

  // default: treat as a normal character
  if (!backslash_ && quotes_ == NO_QUOTES && c <= 32 /* c is a delimiter */) {
    complete_arg();
  } else {
    // [special case] (\<c> inside "") is kept exactly as \<c>
    if (backslash_ && quotes_ == SPECIAL_QUOTES) {
      current_arg_ += '\\';
    }
    current_arg_ += c;
  }
  backslash_ = false;
}

void ParsingState::complete_arg() {
  if (current_arg_.length() > 0) {
    if (io_.has_fd()) {
      current_command_.add_io(io_.with_path(current_arg_));
    } else {
      current_command_.add_arg(current_arg_);
    }
    current_arg_ = "";
    io_ = IOFile();
  }
}

bool ParsingState::complete_command(bool in_final_state) {
  complete_arg(); // whatever is left here is part of the args of this command
  if (io_.has_fd()) {
    // something like (ps aux >) happened; no path specified for io redirection
    error_ = true;
    throw new std::runtime_error(
      "syntax error near unexpected token `newline'");
  }
  completed_ = in_final_state;
  if (!current_command_.args().empty()) {
    parsed_commands_.push_back(current_command_);
    current_command_ = Command();
    return true; // new command added successfuly
  }
  return false; // could not add a new command: command is empty (no args)!
}

};