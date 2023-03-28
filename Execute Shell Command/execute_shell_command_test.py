import execute_shell_command as shell
import unittest
import sys

class TestShellCommand(unittest.TestCase):
    def test_shell_command(self):
        result, status = shell.execute_shell_command('echo Khanna')
        self.assertEqual(result.decode('utf8').rstrip("\r\n"), 'Khanna')

if __name__ == '__main__':
    unittest.main(verbosity=2)

