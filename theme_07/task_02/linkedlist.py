#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: linkedlist.py
Author: omeH
Email: <<>>
Github: https://github.com/omeH
Description:
"""


def isiterable(p_object):
    try:
        iter(p_object)
    except TypeError:
        return False
    else:
        return True


class Node(object):
    """
    Node(value) -> new Node initialized
    """

    value = None
    link = None

    def __init__(self, value):
        """
        N.__init__(value) -- initialized object Node

        >>> node_1 = Node('test')
        >>> node_2 = Node('spam')
        >>> node_1.value, node_2.value
        ('test', 'spam')
        """
        self.value = value

    def __str__(self):
        """
        N.__str__() <==> str(N)

        >>> node = Node('test')
        >>> print(node)
        test
        """
        return '{0}'.format(self.value)

    def __repr__(self):
        """
        N.__repr__() <==> repr(N)

        >>> node = Node('test')
        >>> node.__repr__()
        'test'
        """
        return self.__str__()

    def set_link(self, link):
        """
        N.set_link(link) -- N.link = link
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
    """
    List() -> new empty List
    List(iterable) -> new List initialized from iterable's items
    """

    PRINT_STR = 'linkedlist.List({0})'
    step = 1
    length = 0

    def __init__(self, data=None):
        """
        L.__init__(...) -- initialized object List

        >>> list_1 = List()
        >>> list_2 = List('test')
        >>> list_1.head, list_1.tail
        (None, None)
        >>> isinstance(list_2.head, Node), isinstance(list_2.tail, Node)
        (True, True)
        >>> print(list_2.head)
        t
        >>> list_3 = List(['test'])
        >>> print(list_3.head)
        test
        >>> list_4 = List(list_2)
        >>> len(list_4)
        4
        >>> print(list_4.tail)
        t
        >>> list_5 = List([])
        >>> len(list_5)
        0
        """
        self.head = None
        self.tail = self.head
        if data is None:
            pass
        elif isiterable(data):
            for element in data:
                self.append(element)
        else:
            self.head = Node(data)
            self.tail = self.head
            self.length = 1

    def __len__(self):
        """
        L.__len__() <==> len(L))

        >>> list_1 = List()
        >>> len(list_1)
        0
        >>> list_1 = List('test')
        >>> len(list_1)
        4
        """
        return self.length

    def __iter__(self):
        """
        L.__iter__() <==> iter(L)

        >>> list_1 = List('test')
        >>> it = iter(list_1)
        >>> isinstance(it, ListIter)
        True
        >>> it.next()
        't'
        """
        return ListIter(self)

    def __str__(self):
        """
        L.__str__() <==> str(L)

        >>> list_1 = List(['test', 'spam', 'maps'])
        >>> print(list_1)
        linkedlist.List(['test', 'spam', 'maps'])
        """
        return self.PRINT_STR.format([item for item in self])

    def __repr__(self):
        """
        L.__repr__() <==> repr(L))
        >>> list_1 = List(['test', 'spam', 'maps'])
        >>> print(list_1.__repr__())
        linkedlist.List(['test', 'spam', 'maps'])
        """
        return self.__str__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __ne__(self, other):
        return self.__str__() != other.__str__()

    def __hash__(self):
        return hash(self.__repr__())

    def insert(self, index, value):
        """
        L.insert(index, value) -- insert value before index

            >>> list_1 = List()
            >>> list_1.insert(1, 'test')
            >>> list_1.get()
            'test'
            >>> list_1.insert(1, 'spam')
            >>> list_1.get()
            'test'
            >>> list_1.head.value
            'spam'
            >>> list_1.insert(5, 'maps')
            >>> list_1.get()
            'maps'
            >>> list_1.insert(3, 333)
            >>> for item in list_1:  print(item)
            spam
            test
            333
            maps
        """
        if index < 0:
            index = self.length + index
            index += 1
        # List index out of range
        if index > self.length:
            self.append(value)
            return
        # List has no items
        if self.length == 0:
            self.append(value)
            return
        # Insert item before one items
        if index <= 1:
            self._appstart(value)
            return
        # Decrement the index to insert at the position before the
        # specified index
        index -= 1
        current = self.head
        # decrement the index because current position is set to
        # first item in the 'List'
        index -= 1
        for _ in range(index):
            current = current.link
        node = Node(value)
        node.set_link(current.link)
        current.set_link(node)
        self.length += self.step

    def get(self):
        """
        L.get() -> item -- return the last item on the L

        >>> list_1 = List('test')
        >>> list_1.get()
        't'
        >>> list_1.append('spam')
        >>> list_1.get()
        'spam'
        >>> list_2 = List()
        >>> print(list_2.get())
        None
        """
        if self.tail:
            return self.tail.value
        else:
            return self.tail

    def _appstart(self, element):
        """
        L._appstart(element) -- add element to start L

        >>> list_1 = List()
        >>> list_1._appstart('test')
        >>> list_1.get()
        'test'
        >>> list_1._appstart('spam')
        >>> for item in list_1: print(item)
        spam
        test
        """
        if self.length > 0:
            node = Node(element)
            node.set_link(self.head)
            self.head = node
            self.length += self.step
        else:
            self.append(element)

    def append(self, element):
        """
        L.append(element) -- append element to end L

        >>> list_1 = List('test')
        >>> list_1.tail.value
        't'
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
        self.length += self.step

    def pop(self):
        """
        L.pop() -> item -- remove and return the last item on the L

        >>> list_1 = List('test')
        >>> list_1.append('spam')
        >>> list_1.append('maps')
        >>> list_1.tail.value
        'maps'
        >>> len(list_1)
        6
        >>> list_1.pop()
        'maps'
        >>> len(list_1)
        5
        >>> list_1.tail.value
        'spam'
        """
        if self.length == 0:
            raise IndexError('pop from empty List')
        if self.length == 1:
            head, self.head = self.head, None
            self.length -= self.step
            return head
        current = self.head
        while current.link != self.tail:
            current = current.link
        self.tail = current
        current = current.link
        self.tail.set_link(None)
        self.length -= self.step
        return current.value


class ListIter(object):
    """
    ListIter(obj) -> new ListIter initialized
    """

    current = None

    def __init__(self, obj):
        """
        LI.__init__(obj) -- initialized object ListIter

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
        LI.__iter__() <==> iter(LI)

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
        >>> it.next()
        'test'
        >>> it.next()
        'spam'
        >>> it.next()
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
        return note.value


if __name__ == '__main__':
    import doctest
    doctest.testmod()
