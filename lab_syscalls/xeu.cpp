#include "xeu_utils/StreamParser.h"

#include <iostream>
#include <vector>
#include <cstdio>

using namespace xeu_utils;
using namespace std;

// This function is just to help you learn the useful methods from Command
void command_explanation(const Command& command) {

  /* Methods that return strings (useful for debugging & maybe other stuff) */

  // This prints the command in a format that can be run by our xeu. If you
  // run the printed command, you will get the exact same Command
  cout << "$     repr(): " << command.repr() << endl;

  // args[0] is the command/filename
  cout << "$     args():";
  for (int i = 0; i < command.args().size(); i++) {
    cout << " [" << i << "] " << command.args()[i];
  }
  cout << endl;

  /* Methods that return C-string (useful in exec* syscalls) */

  // this is just the argv[0]
  printf("$ filename(): %s\n", command.filename());

  // This is similar to args, but in the format required by exec* syscalls
  // After the last arg, there is always a NULL pointer (as required by exec*)
  printf("$     argv():");
  for (int i = 0; command.argv()[i]; i++) {
    printf(" [%d] %s", i, command.argv()[i]);
  }
  printf("\n");

}

// This function is just to help you learn the useful methods from Command
void commands_explanation(const vector<Command>& commands) {
  // Shows a representation (repr) of the command you input
  cout << "$ Command::repr(): " << Command::repr(commands) << endl << endl;

  // Shows details of each command
  for (int i = 0; i < commands.size(); i++) {
    cout << "## Command " << i << endl;
    command_explanation(commands[i]);
    cout << endl;
  }
}

int main() {
  // Waits for the user to input a command and parses it. Commands separated
  // by pipe, "|", generate multiple commands. For example, try to input
  //   ps aux | grep xeu
  // And you will notice you have two commands: (ps aux) and (grep xeu)
  // This also handles errors for you. After calling this method you can be
  // sure a command was parsed and is ready to be processed by you.
  const vector<Command> commands = StreamParser().parse().commands();

  // See this method to learn how to use "commands"
  commands_explanation(commands);

  return 0;
}
