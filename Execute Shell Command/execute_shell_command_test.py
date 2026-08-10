import execute_shell_command as shell
import unittest
import sys

class TestShellCommand(unittest.TestCase):
    def test_shell_command(self):
        result, status = shell.execute_shell_command('echo Khanna')
        self.assertEqual(result.decode('utf8').rstrip("\r\n"), 'Khanna')

    def test_shell_command_non_zero_status(self):
        result, status = shell.execute_shell_command('non_existent_command_12345')
        self.assertNotEqual(status, 0)
        self.assertIsInstance(result, bytes)

if __name__ == '__main__':
    unittest.main(verbosity=2)
