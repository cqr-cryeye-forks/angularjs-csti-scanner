import collections
import subprocess
import unittest

from test.tools.LocalAngularServer import LocalAngularServer


class TestPayloads(unittest.TestCase):
    """The TestPayloads class checks if all the payloads pop alerts correctly.

    angular_assets (obj): The AngularJS assets to test.

    """

    angular_assets = collections.OrderedDict([
        ("1.0.0", "https://code.angularjs.org/1.0.0/angular-1.0.0.min.js"),
        ("1.0.1", "https://code.angularjs.org/1.0.1/angular-1.0.1.min.js"),
        ("1.0.2", "https://code.angularjs.org/1.0.2/angular.min.js"),
        ("1.0.3", "https://code.angularjs.org/1.0.3/angular.min.js"),
        ("1.0.4", "https://code.angularjs.org/1.0.4/angular.min.js"),
        ("1.0.5", "https://code.angularjs.org/1.0.5/angular.min.js"),
        ("1.0.6", "https://code.angularjs.org/1.0.6/angular.min.js"),
        ("1.0.7", "https://code.angularjs.org/1.0.7/angular.min.js"),
        ("1.0.8", "https://code.angularjs.org/1.0.8/angular.min.js"),

        ("1.1.0", "https://code.angularjs.org/1.1.0/angular.min.js"),
        ("1.1.1", "https://code.angularjs.org/1.1.1/angular.min.js"),
        ("1.1.2", "https://code.angularjs.org/1.1.2/angular.min.js"),
        ("1.1.3", "https://code.angularjs.org/1.1.3/angular.min.js"),
        ("1.1.4", "https://code.angularjs.org/1.1.4/angular.min.js"),
        ("1.1.5", "https://code.angularjs.org/1.1.5/angular.min.js"),

        ("1.2.0", "https://code.angularjs.org/1.2.0/angular.min.js"),
        ("1.2.1", "https://code.angularjs.org/1.2.1/angular.min.js"),
        ("1.2.2", "https://code.angularjs.org/1.2.2/angular.min.js"),
        ("1.2.3", "https://code.angularjs.org/1.2.3/angular.min.js"),
        ("1.2.4", "https://code.angularjs.org/1.2.4/angular.min.js"),
        ("1.2.5", "https://code.angularjs.org/1.2.5/angular.min.js"),
        ("1.2.6", "https://code.angularjs.org/1.2.6/angular.min.js"),
        ("1.2.7", "https://code.angularjs.org/1.2.7/angular.min.js"),
        ("1.2.8", "https://code.angularjs.org/1.2.8/angular.min.js"),
        ("1.2.9", "https://code.angularjs.org/1.2.9/angular.min.js"),
        ("1.2.10", "https://code.angularjs.org/1.2.10/angular.min.js"),
        ("1.2.11", "https://code.angularjs.org/1.2.11/angular.min.js"),
        ("1.2.12", "https://code.angularjs.org/1.2.12/angular.min.js"),
        ("1.2.13", "https://code.angularjs.org/1.2.13/angular.min.js"),
        ("1.2.14", "https://code.angularjs.org/1.2.14/angular.min.js"),
        ("1.2.15", "https://code.angularjs.org/1.2.15/angular.min.js"),
        ("1.2.16", "https://code.angularjs.org/1.2.16/angular.min.js"),
        ("1.2.17", "https://code.angularjs.org/1.2.17/angular.min.js"),
        ("1.2.18", "https://code.angularjs.org/1.2.18/angular.min.js"),
        ("1.2.19", "https://code.angularjs.org/1.2.19/angular.min.js"),
        ("1.2.20", "https://code.angularjs.org/1.2.20/angular.min.js"),
        ("1.2.21", "https://code.angularjs.org/1.2.21/angular.min.js"),
        ("1.2.22", "https://code.angularjs.org/1.2.22/angular.min.js"),
        ("1.2.23", "https://code.angularjs.org/1.2.23/angular.min.js"),
        ("1.2.24", "https://code.angularjs.org/1.2.24/angular.min.js"),
        ("1.2.25", "https://code.angularjs.org/1.2.25/angular.min.js"),
        ("1.2.26", "https://code.angularjs.org/1.2.26/angular.min.js"),
        ("1.2.27", "https://code.angularjs.org/1.2.27/angular.min.js"),
        ("1.2.28", "https://code.angularjs.org/1.2.28/angular.min.js"),
        ("1.2.29", "https://code.angularjs.org/1.2.29/angular.min.js"),
        ("1.2.30", "https://code.angularjs.org/1.2.30/angular.min.js"),
        ("1.2.31", "https://code.angularjs.org/1.2.31/angular.min.js"),
        ("1.2.32", "https://code.angularjs.org/1.2.32/angular.min.js"),

        ("1.3.0", "https://code.angularjs.org/1.3.0/angular.min.js"),
        ("1.3.1", "https://code.angularjs.org/1.3.1/angular.min.js"),
        ("1.3.2", "https://code.angularjs.org/1.3.2/angular.min.js"),
        ("1.3.3", "https://code.angularjs.org/1.3.3/angular.min.js"),
        ("1.3.4", "https://code.angularjs.org/1.3.4/angular.min.js"),
        ("1.3.5", "https://code.angularjs.org/1.3.5/angular.min.js"),
        ("1.3.6", "https://code.angularjs.org/1.3.6/angular.min.js"),
        ("1.3.7", "https://code.angularjs.org/1.3.7/angular.min.js"),
        ("1.3.8", "https://code.angularjs.org/1.3.8/angular.min.js"),
        ("1.3.9", "https://code.angularjs.org/1.3.9/angular.min.js"),
        ("1.3.10", "https://code.angularjs.org/1.3.10/angular.min.js"),
        ("1.3.11", "https://code.angularjs.org/1.3.11/angular.min.js"),
        ("1.3.12", "https://code.angularjs.org/1.3.12/angular.min.js"),
        ("1.3.13", "https://code.angularjs.org/1.3.13/angular.min.js"),
        ("1.3.14", "https://code.angularjs.org/1.3.14/angular.min.js"),
        ("1.3.15", "https://code.angularjs.org/1.3.15/angular.min.js"),
        ("1.3.16", "https://code.angularjs.org/1.3.16/angular.min.js"),
        ("1.3.17", "https://code.angularjs.org/1.3.17/angular.min.js"),
        ("1.3.18", "https://code.angularjs.org/1.3.18/angular.min.js"),
        ("1.3.19", "https://code.angularjs.org/1.3.19/angular.min.js"),
        ("1.3.20", "https://code.angularjs.org/1.3.20/angular.min.js"),

        ("1.4.0", "https://code.angularjs.org/1.4.0/angular.min.js"),
        ("1.4.1", "https://code.angularjs.org/1.4.1/angular.min.js"),
        ("1.4.2", "https://code.angularjs.org/1.4.2/angular.min.js"),
        ("1.4.3", "https://code.angularjs.org/1.4.3/angular.min.js"),
        ("1.4.4", "https://code.angularjs.org/1.4.4/angular.min.js"),
        ("1.4.5", "https://code.angularjs.org/1.4.5/angular.min.js"),
        ("1.4.6", "https://code.angularjs.org/1.4.6/angular.min.js"),
        ("1.4.7", "https://code.angularjs.org/1.4.7/angular.min.js"),
        ("1.4.8", "https://code.angularjs.org/1.4.8/angular.min.js"),
        ("1.4.9", "https://code.angularjs.org/1.4.9/angular.min.js"),
        ("1.4.10", "https://code.angularjs.org/1.4.10/angular.min.js"),
        ("1.4.11", "https://code.angularjs.org/1.4.11/angular.min.js"),
        ("1.4.12", "https://code.angularjs.org/1.4.12/angular.min.js"),
        ("1.4.13", "https://code.angularjs.org/1.4.13/angular.min.js"),
        ("1.4.14", "https://code.angularjs.org/1.4.14/angular.min.js"),

        ("1.5.0", "https://code.angularjs.org/1.5.0/angular.min.js"),
        ("1.5.1", "https://code.angularjs.org/1.5.1/angular.min.js"),
        ("1.5.2", "https://code.angularjs.org/1.5.2/angular.min.js"),
        ("1.5.3", "https://code.angularjs.org/1.5.3/angular.min.js"),
        ("1.5.4", "https://code.angularjs.org/1.5.4/angular.min.js"),
        ("1.5.5", "https://code.angularjs.org/1.5.5/angular.min.js"),
        ("1.5.6", "https://code.angularjs.org/1.5.6/angular.min.js"),
        ("1.5.7", "https://code.angularjs.org/1.5.7/angular.min.js"),
        ("1.5.8", "https://code.angularjs.org/1.5.8/angular.min.js"),
        ("1.5.9", "https://code.angularjs.org/1.5.9/angular.min.js"),
        ("1.5.10", "https://code.angularjs.org/1.5.10/angular.min.js"),
        ("1.5.11", "https://code.angularjs.org/1.5.11/angular.min.js"),

        ("1.6.0", "https://code.angularjs.org/1.6.0/angular.min.js"),
        ("1.6.1", "https://code.angularjs.org/1.6.1/angular.min.js"),
        ("1.6.2", "https://code.angularjs.org/1.6.2/angular.min.js"),
        ("1.6.3", "https://code.angularjs.org/1.6.3/angular.min.js"),
        ("1.6.4", "https://code.angularjs.org/1.6.4/angular.min.js"),
        ("1.6.5", "https://code.angularjs.org/1.6.5/angular.min.js")
    ])

    def test_payloads(self):
        """Check if every single (stable) AngularJS version throws an alert using ACSTIS."""

        for (version, url) in self.angular_assets.items():
            server = LocalAngularServer()
            server.start(LocalAngularServer.HANDLER_VULNERABLE_TEST, {"asset": url})

            try:
                shell_command = ["python", "acstis.py", "--verify-payload", "--angular-version", version, "--domain",
                                 f"http://{server.url}?vulnerable=payload"]

                print("Testing: " + " ".join(shell_command))

                process = subprocess.Popen(
                    shell_command
                )

                exitcode = process.wait()
            except Exception as e:
                print(f"Exception: {str(e)}")
                exitcode = 1
            server.stop()

            self.assertEqual(exitcode, 0)
