import subprocess
import sys

def execute_shell_command(command):
    """Executes the provided unix shell command """
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return_code = proc.returncode
        if err:
            print(str(err))
        return out, return_code
    except Exception as err:
        print("Exception Occurred while executing module : %s", str(err))
        return 105

if __name__ == '__main__':
    command ='echo Deepak'
    result, status = execute_shell_command(command)
    if status != 0:
        print("Exception in running shell command")
        sys.exit(1)
    else:
        command_result = result.decode('utf8').rstrip("\r\n")
        print(command_result)
