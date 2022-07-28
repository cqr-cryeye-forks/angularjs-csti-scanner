import copy

from nyawc.helpers.URLHelper import URLHelper

from acstis.Payloads import Payloads
from acstis.actions.BaseAction import BaseAction


class QueryDataAction(BaseAction):
    """Add the payload to the GET query data from the queue item.

    Attributes:
        __payloads list(obj): The payloads to add to the query data.

    """

    def __init__(self, payloads):
        """Constructs a QueryDataAction instance.

        Args:
            payloads list(obj): The payloads to add to the query data.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        params = URLHelper.get_ordered_params(self.get_item().request.url)

        if not params:
            return items

        for (key, value) in params.items():
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()
                new_params = copy.deepcopy(params)

                new_params[key] = payload["value"]
                queue_item.payload = payload
                queue_item.request.url = URLHelper.append_with_data(
                    queue_item.request.url,
                    new_params
                )

                new_params[key] = Payloads.get_verify_payload(payload)["value"]
                verify_item.payload = Payloads.get_verify_payload(payload)
                verify_item.request.url = URLHelper.append_with_data(
                    verify_item.request.url,
                    new_params
                )

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
