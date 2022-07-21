import re
import socket
import threading

try:  # Python 3
    from urllib.parse import unquote
except ImportError:  # Python 2
    from urllib import unquote


class LocalAngularServer:
    """The LocalAngularServer class sets up a local vulnerable AngularJS server.

    # Attributes:
    running (bool): If the thread should keep running.
    sock (obj): A reference to the socket.
    data (str): An object with extra data for the handler.
    thread (obj): A reference to the thread.
    url (str): The URL to the local server.
    HANDLER_VULNERABLE_TEST (str): A handler for testing vulnerable applications.
    HANDLER_SCOPE_TEST (str): A handler for testing payloads in certain scopes.

    """

    HANDLER_VULNERABLE_TEST = "handler_vulnerable_test"

    HANDLER_SCOPE_TEST = "handler_scope_test"

    def __init__(self):
        self.thread = None
        self.url = None
        self.sock = None
        self.data = None
        self.running = None

    def start(self, handler, data):
        """Start the websocket to accept HTTP request on localhost.

        Args:
            handler (str): The response handler to use.
            data (obj): An object with extra data for the handler.

        """

        self.running = True
        self.data = data

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(1)

        self.url = f"127.0.0.1:{str(self.sock.getsockname()[1])}"

        self.thread = threading.Thread(target=getattr(self, handler))
        self.thread.start()

    def handler_vulnerable_test(self):
        """Serve a vulnerable AngularJS application for every HTTP request."""

        while self.running:
            try:
                c_sock, caddr = self.sock.accept()
                request = c_sock.recv(1024)

                matches = re.findall(r'GET /\?vulnerable=(.*) HTTP', request.decode("utf-8"))
                vulnerable_value = unquote(matches[0]) if len(matches) == 1 else ""

                html = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <script src='""" + self.data["asset"] + """'></script>
                        </head>
                        <body ng-app="">
                            <a href="?vulnerable=payload">Payload</a>
                            """ + vulnerable_value + """
                        </body>
                    </html>
                """

                c_sock.sendall(b"""HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n""" + bytes(
                    html.encode("UTF-8")))
                c_sock.close()
            except Exception as e:
                print(e)

    def handler_scope_test(self):
        """Serve a vulnerable AngularJS application for every HTTP request."""

        while self.running:
            try:
                c_sock, caddr = self.sock.accept()
                request = c_sock.recv(1024)

                matches = re.findall(r'GET /\?vulnerable=(.*) HTTP', request.decode("utf-8"))
                vulnerable_value = unquote(matches[0]) if len(matches) == 1 else ""

                inside_app = vulnerable_value if self.data["position"] == "inside_app" else ""
                outside_app = vulnerable_value if self.data["position"] == "outside_app" else ""
                inside_non_bindable = vulnerable_value if self.data["position"] == "inside_non_bindable" else ""
                inside_script = vulnerable_value if self.data["position"] == "inside_script" else ""

                html = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <script src='https://code.angularjs.org/1.5.8/angular.min.js'></script>
                        </head>
                        <body>
                            <a href="?vulnerable=payload">Payload</a>
                            <div ng-app="">
                                """ + inside_app + """
                                <p ng-non-bindable><span>""" + inside_non_bindable + """</span></p>
                                <script>""" + inside_script + """</script>
                            </div>
                            """ + outside_app + """
                        </body>
                    </html>
                """

                c_sock.sendall(b"""HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n""" + bytes(
                    html.encode("UTF-8")))
                c_sock.close()
            except Exception as e:
                print(e)

    def stop(self):
        """Stop the websocket."""

        self.running = False
        self.sock.close()
        self.thread.join()
