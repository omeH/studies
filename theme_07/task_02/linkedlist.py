"""
File: linkedlist.py
Author: omeH
Email: <<>>
Github: https://github.com/omeH
Description:
"""


class Node(object):

    value = None
    link = None

    def __init__(self, value):
        """
        >>> node_1 = Node('test')
        >>> node_2 = Node('spam')
        >>> node_1.value, node_2.value
        ('test', 'spam')
        """
        self.value = value

    def __str__(self):
        """
        >>> node = Node('test')
        >>> print(node)
        test
        """
        return str(self.value)

    def set_link(self, link):
        """
        >>> node_1 = Node('test')
        >>> node_2 = Node('spam')
        >>> node_1.set_link(node_2)
        >>> node_2.set_link(node_1)
        >>> node_1.link is node_2
        True
        >>> node_2.link is node_1
        True
        """
        self.link = link


class List(object):

    length = 0

    def __init__(self, data=None):
        """
        >>> list_1 = List()
        >>> list_2 = List('test')
        >>> list_1.head, list_1.tail
        (None, None)
        >>> isinstance(list_2.head, Node), isinstance(list_2.tail, Node)
        (True, True)
        >>> print(list_2.head)
        test
        """
        if data is None:
            self.head = None
            self.tail = self.head
        # elif isinstance(data, list):
        #     self.head = None
        #     for element in data:
        #         self.append(element)
        else:
            self.head = Node(data)
            self.tail = self.head
            self.length = 1

    def __len__(self):
        """
        >>> list_1 = List()
        >>> len(list_1)
        0
        >>> list_1 = List('test')
        >>> len(list_1)
        1
        """
        return self.length

    def __iter__(self):
        """
        >>> list_1 = List('test')
        >>> it = iter(list_1)
        >>> isinstance(it, ListIter)
        True
        >>> it.next().value
        'test'
        """
        return ListIter(self)

    def get(self):
        """
        >>> list_1 = List('test')
        >>> list_1.get().value
        'test'
        >>> list_1.append('spam')
        >>> list_1.get().value
        'spam'
        """
        return self.tail

    def append(self, element):
        """
        >>> list_1 = List('test')
        >>> list_1.tail.value
        'test'
        >>> list_1.append('spam')
        >>> list_1.tail.value
        'spam'
        """
        if self.head is None:
            self.head = Node(element)
            self.tail = self.head
        else:
            node = Node(element)
            self.tail.set_link(node)
            self.tail = node
        self.length += 1

    def pop(self):
        """
        >>> list_1 = List('test')
        >>> list_1.append('spam')
        >>> list_1.append('maps')
        >>> list_1.tail.value
        'maps'
        >>> len(list_1)
        3
        >>> list_1.pop().value
        'maps'
        >>> len(list_1)
        2
        >>> list_1.tail.value
        'spam'
        """
        node = self.head
        while node.link != self.tail:
            node = node.link
        self.tail = node
        node = node.link
        self.tail.set_link(node)
        self.length -= 1
        return node


class ListIter(object):

    current = None

    def __init__(self, obj):
        """
        >>> it = ListIter(List('test'))
        >>> isinstance(it.obj, List)
        True
        >>> isinstance(it.current, Node)
        True
        """
        self.obj = obj
        self.current = obj.head

    def __iter__(self):
        """
        >>> list_1 = List('test')
        >>> it = iter(list_1)
        >>> isinstance(it, ListIter)
        True
        """
        return self

    def next(self):
        """
        >>> list_1 = List()
        >>> list_1.append('test')
        >>> list_1.append('spam')
        >>> list_1.append('maps')
        >>> it = iter(list_1)
        >>> it.next().value
        'test'
        >>> it.next().value
        'spam'
        >>> it.next().value
        'maps'
        >>> it.next()
        Traceback (most recent call last):
            ...
        StopIteration
        """
        if self.current is None:
            raise StopIteration
        note = self.current
        self.current = self.current.link
        return note


if __name__ == '__main__':
    import doctest
    doctest.testmod()
