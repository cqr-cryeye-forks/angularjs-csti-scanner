import signal
import sys
import traceback

import colorlog
from nyawc import Options, Queue
from nyawc.Crawler import Crawler
from nyawc.CrawlerActions import CrawlerActions
from nyawc.QueueItem import QueueItem
from nyawc.helpers.HTTPRequestHelper import HTTPRequestHelper
from nyawc.http.Request import Request
from nyawc.http.Response import Response

from acstis.Scanner import Scanner
from acstis.helpers.BrowserHelper import BrowserHelper
from acstis.helpers.FileLoggingHelper import FileLoggingHelper


class Driver:
    """The main Crawler class which handles the crawling recursion, queue and processes.

    Attributes:
        __args (:class:`argparse.Namespace`): A namespace with all the parsed CLI arguments.
        __options: The options to use for the current crawling runtime.
        __vulnerable_items list(:class:`nyawc.http.Request`): A list of vulnerable items (if any).
        stopping (bool): True on SIGINT, false otherwise.

    """

    def __init__(self, args, options: Options):
        """Constructs a Driver instance. The driver instance manages the crawling proces.

        Args:
            args (:class:`argparse.Namespace`): A namespace with all the parsed CLI arguments.
            options: The options to use for the current crawling runtime.

        """

        self.stopping = False

        self.__args = args
        self.__options = options
        self.__vulnerable_items = []

        self.__options.callbacks.crawler_before_start = self.cb_crawler_before_start
        self.__options.callbacks.crawler_after_finish = self.cb_crawler_after_finish
        self.__options.callbacks.request_before_start = self.cb_request_before_start
        self.__options.callbacks.request_after_finish = self.cb_request_after_finish
        self.__options.callbacks.request_in_thread_after_finish = self.cb_request_in_thread_after_finish
        self.__options.callbacks.request_on_error = self.cb_request_on_error

        self.__options.identity.headers.update({
            "User-Agent": "user_agent(PackageHelper.get_alias(), PackageHelper.get_version())"
        })

        FileLoggingHelper.set_file(self.__args.vulnerable_requests_log)

    def __signal_handler(self, signum, frame):
        """On sigint (e.g. CTRL+C) stop the crawler.

        Args:
            signum (int): The signal number.
            frame (obj): The current stack frame.

        """

        if self.stopping:
            return

        self.stopping = True

        colorlog.getLogger().warning(
            f"Received SIGINT{signum} on frame {frame}, stopping the crawling threads safely. "
            "This could take up to 30 seconds (the thread timeout).")

    def __set_angular_version(self, startpoint: Request):
        """Find and set the AngularJS version as class attribute

        Args:
            startpoint: The startpoint request.

        Returns:
            str: True if found and set, False otherwise.

        """

        if self.__args.angular_version:
            self.__angular_version = self.__args.angular_version
            colorlog.getLogger().info(f"Found AngularJS version {self.__angular_version} in the arguments.")

            return True

        colorlog.getLogger().info("Looking for AngularJS version using a headless browser.")
        colorlog.getLogger().info("Waiting until DOM is completely loaded.")

        self.__angular_version = BrowserHelper.javascript(
            QueueItem(startpoint, Response(self.__args.domain)),
            "return angular.version.full"
        )

        if self.__angular_version:
            colorlog.getLogger().info(f"Found AngularJS version {self.__angular_version}.")
            return True

        colorlog.getLogger().error(
            "Couldn't determine the AngularJS version (`angular.version.full` threw an exception).")
        colorlog.getLogger().error(
            "If you are certain this URL uses AngularJS, specify the version via the `--angular-version` argument.")
        return False

    def start(self):
        """Start the crawler."""

        startpoint = Request(self.__args.domain)
        # startpoint = Request(self.__args.domain, verify=False)
        HTTPRequestHelper.patch_with_options(startpoint, self.__options)

        if self.__set_angular_version(startpoint):
            crawler = Crawler(self.__options)
            signal.signal(signal.SIGINT, self.__signal_handler)

            crawler.start_with(startpoint)

        # Exit the process with the correct status code
        sys.exit(not self.__vulnerable_items)

    @staticmethod
    def cb_crawler_before_start():
        """Called before the crawler starts crawling."""

        colorlog.getLogger().info("Angular CSTI scanner started.")

    def cb_crawler_after_finish(self, queue):
        """Crawler callback (called after the crawler finished).

        Args:
            queue (obj): The current crawling queue.

        """

        if queue.get_all(QueueItem.STATUS_CANCELLED):
            colorlog.getLogger().warning("Angular CSTI scanner finished (but some requests were cancelled).")
        else:
            colorlog.getLogger().info("Angular CSTI scanner finished.")

        if self.__vulnerable_items:
            colorlog.getLogger().success(f"Found {len(self.__vulnerable_items)} vulnerable request(s).")

            colorlog.getLogger().success("Listing vulnerable request(s).")

            for vulnerable_item in self.__vulnerable_items:
                colorlog.getLogger().success(self.__request_to_string(vulnerable_item.request))

                if vulnerable_item.payload["message"]:
                    colorlog.getLogger().warning(vulnerable_item.payload["message"])
        else:
            colorlog.getLogger().warning("Couldn't find any vulnerable requests.")

    def cb_request_before_start(self, queue: Queue, queue_item: QueueItem):
        """Crawler callback (called before a request starts).

        Args:
            queue: The current crawling queue.
            queue_item: The queue item that's about to start.

        Returns:
            str: A crawler action (either DO_SKIP_TO_NEXT, DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        colorlog.getLogger().info(f"Scanning {queue_item.request.url}")

        if self.__vulnerable_items and self.__args.stop_if_vulnerable:
            self.stopping = True
            return CrawlerActions.DO_STOP_CRAWLING

        if self.stopping:
            return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_after_finish(self, queue: Queue, queue_item: QueueItem, new_queue_items: list[QueueItem]):
        """Crawler callback (called after a request finished).

        Args:
            queue: The current crawling queue.
            queue_item: The queue item that was finished.
            new_queue_items: The new queue items that were found

        Returns:
            str: A crawler action (either DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        self.__vulnerable_items.extend(queue_item.vulnerable_items)

        for vulnerable_item in queue_item.vulnerable_items:
            colorlog.getLogger().success(self.__request_to_string(vulnerable_item.request))
            FileLoggingHelper.log(self.__request_to_string(vulnerable_item.request))

            if vulnerable_item.payload["message"]:
                colorlog.getLogger().warning(vulnerable_item.payload["message"])

        if self.__vulnerable_items and self.__args.stop_if_vulnerable:
            self.stopping = True
            return CrawlerActions.DO_STOP_CRAWLING

        if self.stopping:
            return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    @staticmethod
    def cb_request_on_error(queue_item: QueueItem, message: str):
        """Crawler callback (called when a request error occurs).

        Args:
            queue_item: The queue item that failed.
            message (str): The error message.

        """

        colorlog.getLogger().error(f"{queue_item}: {message}")

    def cb_request_in_thread_after_finish(self, queue_item: QueueItem):
        """Crawler callback (called after a request finished).

        Args:
            queue_item: The queue item that's about to start.

        Note:
            This method gets called in the crawling thread and is therefore not thread safe.

        """

        queue_item.vulnerable_items = []

        if self.stopping or not hasattr(queue_item.response, "text"):
            return

        try:
            queue_item.vulnerable_items = Scanner(self, self.__angular_version, self.__args.verify_payload,
                                                  queue_item).get_vulnerable_items()
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    @staticmethod
    def __request_to_string(request: Request):
        """Convert the given requests to a string representation.

        Args:
            request: The request to convert.

        Returns:
            str: The string representation

        """

        data = ""

        if request.data:
            key_values = [f"{key}={value}" for key, value in request.data.items()]
            data += "&".join(key_values)

        return f"{request.method.upper()}({data}): {request.url}"


class Namespace:
    """An ArgumentParser namespace mockup for if the driver is called manually (using code instead of CLI)."""

    def __init__(self, **kwargs):
        """Initialize the namespace with the given arguments."""

        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        """Return values that exists, otherwise return None.

        Args:
            name (str): The name of the key to look for.

        Returns:
            str: The value in the dict or None.

        """

        return object.__getattribute__(self, name) if name in self.__dict__ else None
