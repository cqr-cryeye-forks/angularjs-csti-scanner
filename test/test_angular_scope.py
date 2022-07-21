import subprocess
import unittest

from test.tools.LocalAngularServer import LocalAngularServer


class TestAngularScope(unittest.TestCase):
    """The TestAngularScope class checks if payloads are detected correctly (without using PhantomJS)."""

    def test_inside_app(self):
        """Payloads inside the AngularJS app should be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_app"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain",
                             f"http://{server.url}?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print(f"Exception: {str(e)}")
            exitcode = 1
        server.stop()

        self.assertEqual(exitcode, 0)

    def test_outside_app(self):
        """Payloads outside the AngularJS app shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "outside_app"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain",
                             f"http://{server.url}?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print(f"Exception: {str(e)}")
            exitcode = 1
        server.stop()

        self.assertNotEqual(exitcode, 0)

    def test_inside_non_bindable(self):
        """Payloads inside the non bindable attributes shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_non_bindable"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain",
                             f"http://{server.url}?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print(f"Exception: {str(e)}")
            exitcode = 1
        server.stop()

        self.assertNotEqual(exitcode, 0)

    def test_inside_script(self):
        """Payloads inside a script tag shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_script"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain",
                             f"http://{server.url}?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print(f"Exception: {str(e)}")
            exitcode = 1
        server.stop()

        self.assertNotEqual(exitcode, 0)
