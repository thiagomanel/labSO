#include "__lib__/catch.hpp"
#include "../IOFile.h"
#include <iostream>

using namespace xeu_utils;

TEST_CASE("[IOFile] constructor and getters", "[IOFile]") {
  {
    IOFile io;
    const int INVALID_FD = IOFile::INVALID_FD;

    // the initial fd should be invalid
    REQUIRE(!io.has_fd());
    REQUIRE(io.fd() == INVALID_FD);
  }

  {
    int fd = 2;
    bool is_input = true;
    std::string path = "somePath";
    IOFile io(fd, is_input, path);

    REQUIRE(io.has_fd());
    REQUIRE(io.fd() == fd);
    REQUIRE(io.is_input() == is_input);
    REQUIRE(io.is_output() != is_input);
    REQUIRE(io.path() == path);
  }

  {
    int fd = 3;
    bool is_input = false;
    std::string path = "somePath2";
    IOFile io(fd, is_input, path);

    REQUIRE(io.fd() == fd);
    REQUIRE(io.is_output() != is_input);
    REQUIRE(io.path() == path);
  }
}

TEST_CASE("[IOFile] with_*()", "[IOFile]") {
  int fd = 11;
  bool input = true;
  std::string path = "testPath";

  REQUIRE(IOFile().with_fd(fd).fd() == fd);
  REQUIRE(IOFile().with_input(input).is_input() == input);
  REQUIRE(IOFile().with_input(!input).is_input() == !input);
  REQUIRE(IOFile().with_path(path).path() == path);
}

TEST_CASE("[IOFile] immutability in getters and setters", "[IOFile]") {
  int original_fd = 11;
  bool original_input = true;
  std::string original_path = "testPath";
  IOFile io(original_fd, original_input, original_path);

  int fd = original_fd + 1;
  bool input = !original_input;
  std::string path = original_path + "/with";

  // setters
  {
    io.with_fd(fd);
    REQUIRE(io.fd() == original_fd);

    io.with_input(input);
    REQUIRE(io.is_input() == original_input);

    io.with_path(path);
    REQUIRE(io.path() == original_path);
  }

  // getters
  {
    int&& fd = io.fd();
    fd++;
    REQUIRE(io.fd() == original_fd);

    bool&& input = io.is_input();
    input = !input;
    REQUIRE(io.is_input() == original_input);

    io.path() += "/mutatePathReturn";
    REQUIRE(io.path() == original_path);
  }
}

TEST_CASE("[IOFile] repr()", "[IOFile]") {
  REQUIRE(IOFile(11, true, "/path/in").repr() == "11</path/in");
  REQUIRE(IOFile(11, false, "/path/out").repr() == "11>/path/out");
  REQUIRE(IOFile(2, false, "/path/err").repr() == "2>/path/err");
  REQUIRE(IOFile(0, true, "/path/stdin").repr() == "</path/stdin");
  REQUIRE(IOFile(1, false, "/path/stdout").repr() == ">/path/stdout");
  REQUIRE(IOFile(0, false, "/path/stdin/isOut").repr() == "0>/path/stdin/isOut");
  REQUIRE(IOFile(1, true, "/path/stdout/isIn").repr() == "1</path/stdout/isIn");

  // escaping
  REQUIRE(IOFile(3, true, "with space").repr() == "3<\"with space\"");
}
