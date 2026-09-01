import unittest
import execute_shell_command as shell

class TestShellCommand(unittest.TestCase):
    def test_shell_command_bytes(self):
        result, status = shell.execute_shell_command('echo Khanna')
        self.assertEqual(status, 0)
        output_str = result.decode('utf-8', errors='replace').rstrip("\r\n").strip()
        self.assertEqual(output_str, 'Khanna')

    def test_shell_command_text_mode(self):
        result, status = shell.execute_shell_command('echo Khanna', text=True)
        self.assertEqual(status, 0)
        self.assertEqual(result.strip(), 'Khanna')

if __name__ == '__main__':
    unittest.main(verbosity=2)


