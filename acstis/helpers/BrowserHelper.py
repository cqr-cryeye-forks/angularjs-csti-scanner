import ctypes
import json
import os
import stat
import sys

import requests
import requests.cookies
from nyawc import QueueItem
from nyawc.helpers.HTTPRequestHelper import HTTPRequestHelper
from nyawc.http.Request import Request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from constants import FILE_PATH

try: # Python 3
    from urllib.parse import quote, urlparse
except:  # Python 2
    from urllib import quote
    from urlparse import urlparse


class BrowserHelper:
    """The BrowserHelper enables headless web browsing.

    _phantomjs_driver (str): The cached path to the executable PhantomJS driver.

    """

    _phantomjs_driver = None

    @staticmethod
    def request(queue_item: QueueItem):
        """Execute the given queue item and return the browser instance.

        Args:
            queue_item: The queue item to execute the JavaScript on.

        Returns:
            obj: The browser instance reference.

        """

        try:
            browser = BrowserHelper.__get_browser(queue_item)

            if queue_item.request.method == Request.METHOD_POST:
                browser.get('about:blank')
                browser.execute_script(
                    'window.doRequest=function(a,b,c){c=c||"post";var d=document.createElement("form");d.'
                    'setAttribute("method",c),d.setAttribute("action",a),b=decodeURIComponent(b),b=JSON.parse(b);'
                    'for(var e in b)if(b.hasOwnProperty(e)){var f=document.createElement("input");f.setAttribute('
                    '"type","hidden"),f.setAttribute("name",e),f.setAttribute("value",b[e]),d.appendChild(f)}documen'
                    't.body.appendChild(d),d.submit()}')
                browser.execute_script('window.doRequest("{}", `{}`, "{}");'.format(queue_item.request.url, quote(
                    json.dumps(queue_item.request.data)), queue_item.request.method))
            else:
                browser.get(queue_item.request.url)

            return browser
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def javascript(queue_item: QueueItem, command):
        """Execute a JavaScript command on the given queue item.

        Args:
            queue_item: The queue item to execute the JavaScript on.
            command (str): The JavaScript command.

        Returns:
            str: The response of the JavaScript command.

        """

        try:
            browser = BrowserHelper.request(queue_item)
            response = browser.execute_script(command)
            browser.quit()
        except Exception as e:
            print(e)
            response = None

        return response

    @staticmethod
    def __get_browser(queue_item: QueueItem = None):
        """Get the PhantomJS browser.

        Args:
            queue_item: Use authentication/headers/cookies etc from this queue item (if given).

        Returns:
            obj: The PhantomJS Selenium object.

        """

        capabilities = dict(DesiredCapabilities.HTMLUNITWITHJS)
        service = []

        if queue_item:

            # Add authentication header to request
            if queue_item.request.auth:
                queue_item.request.auth(queue_item.request)

            # Add cookie header to request
            if queue_item.request.cookies:
                cookie_string = HTTPRequestHelper.get_cookie_header(queue_item)
                queue_item.request.headers["Cookie"] = cookie_string

            # Add headers to PhantomJS
            if queue_item.request.headers:
                default_headers = requests.utils.default_headers()
                for (key, value) in queue_item.request.headers.items():
                    if key.lower() == "user-agent":
                        capabilities["phantomjs.page.settings.userAgent"] = value
                    # PhantomJS has issues with executing JavaScript on pages with GZIP encoding.
                    # See link for more information (https://github.com/detro/ghostdriver/issues/489).
                    elif key != "Accept-Encoding" or "gzip" not in value:
                        capabilities[f"phantomjs.page.customHeaders.{key}"] = value

            # Proxies
            if queue_item.request.proxies:
                service.extend(BrowserHelper.__proxies_to_service_args(queue_item.request.proxies))

        driver_path = BrowserHelper.__get_phantomjs_driver()
        return webdriver.Chrome(
            executable_path=driver_path,
            desired_capabilities=capabilities,
            service_args=service
        )

    @staticmethod
    def __proxies_to_service_args(proxies):
        """Get the proxy details in a service args array.

        Args:
            proxies (obj): An `requests` proxies object.

        Returns:
            list: The service args containing proxy details

        Note:
            The `ignore-ssl-errors` argument is also added because
            all SSL checks are handled by Python's requests module.
            Python's requests module is also able to allow certain
            custom certificates (e.g. if a proxy is used).

        """

        service_args = []

        parsed = urlparse(list(proxies.values())[0])

        # Proxy type
        if parsed.scheme.startswith("http"):
            service_args.append("--proxy-type=http")
        else:
            service_args.append(f"--proxy-type={parsed.scheme}")

        # Proxy
        host_and_port = parsed.netloc.split("@")[-1]
        service_args.append(f"--proxy={host_and_port}")

        # Proxy auth
        if len(parsed.netloc.split("@")) == 2:
            user_pass = parsed.netloc.split("@")[0]
            service_args.append(f"--proxy-auth={user_pass}")

        # Ignore SSL (please see note in this method).
        service_args.append("--ignore-ssl-errors=true")

        return service_args

    @staticmethod
    def __get_phantomjs_driver():
        """Get the path to the correct PhantomJS driver.

        Returns:
            str: The location of the driver.

        """

        if BrowserHelper._phantomjs_driver:
            return BrowserHelper._phantomjs_driver

        path = FILE_PATH.joinpath('acstis', 'phantomjs')
        bits = ctypes.sizeof(ctypes.c_voidp)
        x = "32" if bits == 4 else "64"

        if sys.platform in ["linux", "linux2"]:
            file = path.joinpath(f"linux{x}-2.1.1").as_posix()
        elif sys.platform == "darwin":
            file = path.joinpath("mac-2.1.1").as_posix()
        elif sys.platform == "win32":
            file = path.joinpath("win-2.1.1.exe").as_posix()

        st = os.stat(file)
        os.chmod(file, st.st_mode | stat.S_IEXEC)

        BrowserHelper._phantomjs_driver = file
        return BrowserHelper._phantomjs_driver
