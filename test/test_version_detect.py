import unittest

from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response

from acstis.helpers.BrowserHelper import BrowserHelper
from test.tools.LocalAngularServer import LocalAngularServer


class TestVersionDetect(unittest.TestCase):
    """The TestVersionDetect class checks if the AngularJS versions are detected correctly."""

    def test_version_detect(self):
        """Check if a single (stable) AngularJS version is detected by ACSTIS."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_VULNERABLE_TEST,
                     {"asset": "https://code.angularjs.org/1.5.8/angular.min.js"})

        domain = f"http://{server.url}?vulnerable=payload"

        version = BrowserHelper.javascript(
            QueueItem(Request(domain), Response(domain)),
            "return angular.version.full"
        )

        server.stop()

        self.assertEqual("1.5.8", version)
