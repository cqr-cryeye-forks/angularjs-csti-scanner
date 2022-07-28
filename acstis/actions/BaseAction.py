import copy
from urllib.parse import urlparse

from nyawc.QueueItem import QueueItem
from nyawc.http.Response import Response


class BaseAction(object):
    """The BaseAction can be used to create other actions.

    Attributes:
        __queue_item: The queue item containing the response to scrape.

    """

    def __init__(self, __queue_item: QueueItem = None):
        self.__queue_item = __queue_item

    def get_action_items_derived(self) -> list:
        """
        return processed data
        """
        return []

    def get_action_items(self, queue_item: QueueItem) -> list[QueueItem]:
        """Get new queue items that could be vulnerable.

        Args:
            queue_item: The queue item containing a response the scrape.

        Returns:
            A list of new queue items that were found.

        """

        self.__queue_item = queue_item
        return self.get_action_items_derived()

    def get_item(self) -> QueueItem:
        """Get the original queue item.

        Returns:
         The original queue item.

        """

        return self.__queue_item

    def get_item_copy(self) -> QueueItem:
        """Copy the current queue item.

        Returns:
            :class:`nyawc.QueueItem`: A copy of the current queue item.

        """

        request = copy.deepcopy(self.__queue_item.request)
        return QueueItem(request, Response(request.url))

    def get_parsed_url(self, url=None):
        """Get the parsed URL.

        Args:
            url (str): The URL to parse (None will use the queue item URL)

        Returns:
            ParseResult: The parsed URL.

        """

        if url:
            return urlparse(url)

        if not hasattr(self.__queue_item.request, 'url_parsed'):
            url_parsed = urlparse(self.__queue_item.request.url)
            self.__queue_item.request.url_parsed = url_parsed

        return self.__queue_item.request.url_parsed

    def get_filename(self):
        """Get the filename from the current queue item URL, if exists.

        Returns:
            str: The filename, or None if it does not exist.

        """
        filename = self.get_parsed_url().path.split("/")[-1]
        return filename if "." in filename else None
