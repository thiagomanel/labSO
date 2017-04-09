#include "xeu_utils/StreamParser.h"

#include <iostream>
#include <vector>

using namespace xeu_utils;
using namespace std;

int main() {
  ParsingState p = StreamParser().parse();
  // cout << p.dump();
  // vector<Command> commands = p.commands();
  return 0;
}