from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
