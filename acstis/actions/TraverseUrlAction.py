from acstis.Payloads import Payloads
from acstis.actions.BaseAction import BaseAction


class TraverseUrlAction(BaseAction):
    """Traverse the payload in the URL from the queue item.

    Attributes:
        __payloads list(obj): The payloads to traverse in the URL.

    """

    def __init__(self, payloads):
        """Constructs a TraverseUrlAction instance.

        Args:
            payloads list(obj): The payloads to traverse in the URL.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        path = self.get_parsed_url().path
        if filename := self.get_filename():
            path = path[:-len(filename)]

        parts = list(filter(None, path.split("/")))

        for index in range(len(parts)):
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()
                path = "/".join(parts[:index])

                path_with_affix = ("/" if path else "") + path + "/" + payload["value"]
                parsed = self.get_parsed_url(queue_item.request.url)
                parsed = parsed._replace(path=path_with_affix, query="")
                queue_item.request.url = parsed.geturl()
                queue_item.payload = payload

                path_with_affix = ("/" if path else "") + path + "/" + Payloads.get_verify_payload(payload)["value"]
                parsed = self.get_parsed_url(verify_item.request.url)
                parsed = parsed._replace(path=path_with_affix, query="")
                verify_item.request.url = parsed.geturl()
                verify_item.payload = Payloads.get_verify_payload(payload)

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
