import subprocess
import sys

def execute_shell_command(command: str, text: bool = False, timeout: float = None):
    """Executes the provided shell command safely across operating systems."""
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate(timeout=timeout)
        return_code = proc.returncode

        if err:
            err_msg = err.decode('utf-8', errors='replace') if isinstance(err, bytes) else str(err)
            if err_msg.strip():
                print("Stderr: %s" % err_msg.strip())

        if text and isinstance(out, bytes):
            out = out.decode('utf-8', errors='replace').rstrip("\r\n")

        return out, return_code
    except Exception as err:
        print("Exception Occurred while executing module : %s" % str(err))
        return 105, 105

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'echo Deepak'
    result, status = execute_shell_command(cmd, text=True)
    if status != 0:
        print("Exception in running shell command (Status: %s)" % status)
        sys.exit(1)
    else:
        print(result)

if __name__ == '__main__':
    main()

