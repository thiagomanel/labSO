#include "xeu_utils/StreamParser.h"

#include <iostream>
#include <vector>

using namespace xeu_utils;
using namespace std;

int main() {
  ParsingState p = StreamParser().parse();
  cout << p.dump();
  vector<Command> commands = p.commands();

   for (int index = 0; index + 1 < commands.size(); index++) {
	Command& command = commands[i];

	printf("%-3d %-30s %-6d %-5d %-5d %-10lld %-10lld %-3d\n",
								                index, command.originalCommand.c_str(), command.processId,
										          command.userId, command.groupId, (long long)command.startEpoch,
											            (long long)command.endEpoch, command.retnCode
												            );
					          }

  return 0;
}
