import requests
from nyawc.QueueItem import QueueItem
from nyawc.http.Handler import Handler as HTTPHandler
from requests import adapters

from acstis.Payloads import Payloads
from acstis.actions.FormDataAction import FormDataAction
from acstis.actions.QueryDataAction import QueryDataAction
from acstis.actions.TraverseUrlAction import TraverseUrlAction
from acstis.helpers.BrowserHelper import BrowserHelper


class Scanner:
    """The Scanner scans specific queue items on sandbox escaping/bypassing.

    Attributes:
        scanned_hashes list(str): A list of scanned queue item hashes.
        __actions list(:class:`acstis.actions.BaseAction`): The actions to perform on the queue item.
        __driver: Used to check if we should stop scanning.
        __verify_payload (bool): Verify if the payload was executed.
        __queue_item (:class:`nyawc.QueueItem`): The queue item to perform actions on.
        __session (obj): A Python requests session.

    """

    scanned_hashes = []

    def __init__(self, driver, angular_version: str, verify_payload: bool, queue_item: QueueItem):
        """Initialize a scanner for the given queue item.

        Args:
            driver: (:class: Driver) Used to check if we should stop scanning.
            angular_version (str): The AngularJS version of the given queue_item (e.g. `1.4.2`).
            verify_payload (bool): Verify if the payload was executed.
            queue_item: The queue item to scan.

        """

        self.__driver = driver
        self.__verify_payload = verify_payload
        self.__queue_item = queue_item
        self.__session = requests.Session()

        self.__session.mount('http://', adapters.HTTPAdapter(max_retries=2))
        self.__session.mount('https://', adapters.HTTPAdapter(max_retries=2))

        self.__actions = [
            TraverseUrlAction(Payloads.get_for_version(angular_version)),
            FormDataAction(Payloads.get_for_version(angular_version)),
            QueryDataAction(Payloads.get_for_version(angular_version))
        ]

    def get_vulnerable_items(self) -> list[QueueItem]:
        """Get a list of vulnerable queue items, if any.

        Returns:
            A list of vulnerable queue items.

        """

        results = []

        for action in self.__actions:
            if self.__driver.stopping:
                break

            items = action.get_action_items(self.__queue_item)

            for item in items:
                if self.__driver.stopping:
                    break

                if item.get_hash() in self.scanned_hashes:
                    continue

                self.scanned_hashes.append(item.get_hash())

                if self.__is_item_vulnerable(item):
                    results.append(item)

        return results

    def __is_item_vulnerable(self, queue_item: QueueItem) -> bool:
        """
        Check if the given queue item is vulnerable by executing it using the HttpHandler
        and checking if the payload is in scope.

        Args:
            queue_item: The queue item to check.

        Returns:
            bool: True if vulnerable, false otherwise.

        """
        try:
            HTTPHandler(None, queue_item)
        except Exception as e:
            print(e)
            return False
        if not queue_item.response.headers.get("content-type") \
                or "html" not in queue_item.response.headers.get("content-type"):
            return False
        if not queue_item.get_soup_response():
            return False
        return bool(not self.__verify_payload
                    or self.__verify_queue_item(queue_item.verify_item)) if self.__should_payload_execute(queue_item) \
            else False

    @staticmethod
    def __should_payload_execute(queue_item: QueueItem):
        """Run static checks to see if the payload should be executed.

        Args:
            queue_item: The queue item to check.

        Returns:
            bool: True if payload should execute, false otherwise.

        """

        soup = queue_item.get_soup_response()

        ng_app_soup = soup.select("[ng-app]")
        if not ng_app_soup:
            return False

        for non_bindable in ng_app_soup[0].select("[ng-non-bindable]"):
            non_bindable.decompose()

        in_scope_html = str(ng_app_soup[0])

        return queue_item.payload["value"] in in_scope_html

    @staticmethod
    def __verify_queue_item(queue_item: QueueItem) -> bool:
        """Verify if the browser opened a new window.

        Args:
            queue_item: The queue item to check.

        Returns:
            bool: True if the payload worked, false otherwise.

        """

        browser = BrowserHelper.request(queue_item)
        return browser and len(browser.window_handles) >= 2
