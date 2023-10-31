import execute_shell_command as shell
import sys

if __name__ == '__main__':
    #Shell command to execute
    command ='echo Khanna'

    #Call execute_shell_command function from execute_shell_command.py script, result will have result return from shell command, status will have status of that command
    result, status = shell.execute_shell_command(command)

    #Check status of command ran, status != 0 means command failed
    if status != 0:
        print("Exception in running shell command")
        sys.exit(1)
    else:
        # Take required action on result return after running shell command
        command_result = result.decode('utf8').rstrip("\r\n")
        print(command_result)
