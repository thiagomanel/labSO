#pragma once

#include "IOFile.h"

#include <string>

namespace xeu_utils {

struct ArgumentUtils {
  /**
   * Escapes an arg and embeds it in double quotes.
   */
  static std::string escape(const std::string& unescaped_arg);

  /**
   * Escapes an arg and embeds it in double quotes if needed. If escaping is
   * not necessary, just returns the arg unmodified. See requires_escaping().
   */
  static std::string escape_if_needed(const std::string& unescaped_arg);

 private:
  /**
   * Returns whether a character inside an arg would require escaping or not.
   */
  static bool requires_escaping(char c);
};

};