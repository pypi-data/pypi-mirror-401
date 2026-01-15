from typing import Iterator


class CachedIterator:
    def __init__(self, iterator: Iterator):
        """Wrap an iterable so that it functions like a list, but
        does so in a lazy manner. I.e. getting an item by a single index
        or index slice will consume the iterable up to that index,
        cache the items, and return the result. If the index has already
        been consumed, the cached items will be used.

        Args:
            iterable (_type_): Iterable
        """
        self.iterator = iterator
        self.current_index = -1
        self.cached_items = []
        self.done = False

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                raise IndexError("Negative indexing is not supported")
            max_index = index
        elif isinstance(index, slice):
            if index.start is not None and index.start < 0:
                raise IndexError("Negative indexing is not supported")
            if index.stop is None or index.stop < 0:
                raise IndexError("Negative indexing is not supported")
            max_index = index.stop - 1
        else:
            raise TypeError("Invalid index type")

        while self.current_index < max_index:
            try:
                item = next(self.iterator)
                self.cached_items.append(item)
                self.current_index += 1
            except StopIteration:
                self.done = True
                break

        return self.cached_items[index]

    def __len__(self):
        while True:
            try:
                item = next(self.iterator)
                self.cached_items.append(item)
                self.current_index += 1
            except StopIteration:
                self.done = True
                break

        return len(self.cached_items)
