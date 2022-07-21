from acstis.Payloads import Payloads
from acstis.actions.BaseAction import BaseAction


class FormDataAction(BaseAction):
    """Add the payload to the POST form data from the queue item.

    Attributes:
        __payloads list(obj): The payloads to add to the form data.

    """

    def __init__(self, payloads):
        """Constructs a FormDataAction instance.

        Args:
            payloads list(obj): The payloads to add to the form data.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        if not self.get_item().request.data:
            return items

        for (key, value) in self.get_item().request.data.items():
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()

                queue_item.request.data[key] = payload["value"]
                queue_item.payload = payload

                verify_item.request.data[key] = Payloads.get_verify_payload(payload)["value"]
                verify_item.payload = Payloads.get_verify_payload(payload)

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
