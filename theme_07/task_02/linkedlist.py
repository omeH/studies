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
    except TypeError, error:
        raise error
    else:
        return True


class _ListSelfLinkError(Exception):
    pass


class _Node(object):
    """
    Node(value) -> new Node initialized
    """

    value = None
    link = None

    def __init__(self, value):
        """
        N.__init__(value) -- initialized object Node

        >>> node_1 = _Node('test')
        >>> node_2 = _Node('spam')
        >>> node_1.value, node_2.value
        ('test', 'spam')
        """
        self.value = value

    def __str__(self):
        """
        N.__str__() <==> str(N)

        >>> node = _Node('test')
        >>> print(node)
        test
        """
        return '{0}'.format(self.value)

    def __repr__(self):
        """
        N.__repr__() <==> repr(N)

        >>> node = _Node('test')
        >>> node.__repr__()
        'test'
        """
        return self.__str__()

    def __cmp__(self, other):
        if isinstance(other, _Node):
            return cmp(self.value, other.value)
        return cmp(self.value, other)

    def set_link(self, link):
        """
        N.set_link(link) -- N.link = link

        >>> node_1 = _Node('test')
        >>> node_2 = _Node('spam')
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
    List() -> new empty List.
    List(iterable) -> new List initialized from iterable's items.
    """

    PRINT_STR = 'linkedlist.List({0})'
    CMP_NEGATIVE = -1
    CMP_ZERO = 0
    CMP_POSITIVE = 1
    step = 1
    length = 0
    depth = 0
    max_depth = 20

    def __init__(self, data=None):
        """
        L.__init__(...) -- initialized object List.

        >>> list_1 = List()
        >>> list_2 = List('test')
        >>> list_1.head, list_1.tail
        (None, None)
        >>> isinstance(list_2.head, _Node), isinstance(list_2.tail, _Node)
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
        >>> isinstance(it, _ListIter)
        True
        >>> it.next()
        't'
        """
        return _ListIter(self)

    def __str__(self):
        """
        L.__str__() <==> str(L)

        >>> list_1 = List(['test', 'spam', 'maps'])
        >>> print(list_1)
        ['test', 'spam', 'maps']
        """
        self.depth += 1
        if self.depth >= self.max_depth:
            raise _ListSelfLinkError()
        try:
            msg = '{0}'.format([item for item in self])
        except _ListSelfLinkError:
            if self.depth > 2:
                raise
            msg = '[[...]]'
        finally:
            self.depth -= 1
        return msg
        """
        result = []
        for item in self:
            if item is self:
                return '[[...]]'
            result.append(item)
        return '{0}'.format(result)
        """

    def __repr__(self):
        """
        L.__repr__() <==> repr(L))

        >>> list_1 = List(['test', 'spam', 'maps'])
        >>> print(list_1.__repr__())
        linkedlist.List(['test', 'spam', 'maps'])
        """
        return self.PRINT_STR.format(self.__str__())

    def __add__(self, other):
        """
        L.__add__(item) <==> L + item

        >>> list_1 = List(['test', 'maps'])
        >>> list_2 = List(['spam', 'food'])
        >>> list_1 + list_2
        linkedlist.List(['test', 'maps', 'spam', 'food'])
        >>> list_1
        linkedlist.List(['test', 'maps'])
        >>> list_1 + 'test'
        Traceback (most recent call last):
            ...
        TypeError: can only concatenate List to List
        """
        if not isinstance(other, List):
            raise TypeError('can only concatenate List to List')
        result = List(self)
        for item in other:
            result.append(item)
        return result

    def __iadd__(self, other):
        """
        L.__iadd__(Y) <==> L += Y

        >>> list_1 = List(['test', 'spam'])
        >>> list_2 = List(['maps', 'food'])
        >>> list_1 += list_2
        >>> list_1
        linkedlist.List(['test', 'spam', 'maps', 'food'])
        """
        # Creating a new List is necessary in order to in the
        # event of: L += L; was not triggered by an infinite
        # cycle.
        if self is other:
            new = List(other)
        else:
            new = other

        for item in new:
            self.append(item)
        return self

    def __cmp__(self, other):
        """
        L.__cmp__(Y) -> integer <==> cmp(L, Y)
        Return negative if L<Y, zero if L=Y, positive if L>Y.

        >>> list_1 = List('test')
        >>> list_2 = List('spam')
        >>> list_1.__cmp__(list_2)
        1
        >>> list_2.__cmp__(list_1)
        -1
        >>> list_1.__cmp__(list_1)
        0
        """
        if not isinstance(other, List):
            return cmp(hash(self), hash(other))
        # Select master List which is less than the length.
        # It is necessary that would  not out of range of one
        # of them. Variable 'order' determines the pattern
        # comparison: [self, other].
        if cmp(self.length, other.length) == self.CMP_POSITIVE:
            first_current = other.head
            second_current = self.head
            order = [second_current, first_current]
        else:
            first_current = self.head
            second_current = other.head
            order = [first_current, second_current]
        # Cycle performs a search of the first inequality of
        # Lists items.
        while first_current is not None:
            result = cmp(*order)
            if result == self.CMP_NEGATIVE:
                return self.CMP_NEGATIVE
            elif result == self.CMP_POSITIVE:
                return self.CMP_POSITIVE
            else:
                first_current = first_current.link
                second_current = second_current.link
        # If cycle performs is successful, it means that there
        # may be three situations:
        # 1) List are equal, if equal to the length;
        # 2) self is less, if the length of the self is less
        #    than the length of the other.
        # 3) self is more, if the length of the self is more
        #    than the length of the other.
        if cmp(self.length, other.length) == self.CMP_ZERO:
            return self.CMP_ZERO
        elif cmp(self.length, other.length) == self.CMP_NEGATIVE:
            return self.CMP_NEGATIVE
        return self.CMP_POSITIVE

    def __eq__(self, other):
        """
        L.__eq__(Y) <==> L == Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 == list_2
        True
        >>> list_1.remove('t')
        >>> list_1 == list_2
        False
        """
        if self.__cmp__(other) == self.CMP_ZERO:
            return True
        return False

    def __ne__(self, other):
        """
        L.__ne__(Y) <==> L != Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 != list_2
        False
        >>> list_1.remove('t')
        >>> list_1 != list_2
        True
        """
        if self.__cmp__(other) != self.CMP_ZERO:
            return True
        return False

    def __gt__(self, other):
        """
        L.__gt__(Y) <==> L > Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 > list_2
        False
        >>> list_2.remove('t')
        >>> list_1 > list_2
        True
        """
        if self.__cmp__(other) == self.CMP_POSITIVE:
            return True
        return False

    def __lt__(self, other):
        """
        L.__lt__(Y) <==> L < Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 < list_2
        False
        >>> list_1.remove('t')
        >>> list_1 < list_2
        True
        """
        if self.__cmp__(other) == self.CMP_NEGATIVE:
            return True
        return False

    def __ge__(self, other):
        """
        L.__ge__(Y) <==> L >= Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 >= list_2
        True
        >>> list_1.remove('t')
        >>> list_1 >= list_2
        False
        >>> list_2 >= list_1
        True
        """
        if self.__cmp__(other) != self.CMP_NEGATIVE:
            return True
        return False

    def __le__(self, other):
        """
        L.__le__(Y) <==> L <= Y

        >>> list_1 = List('test')
        >>> list_2 = List('test')
        >>> list_1 <= list_2
        True
        >>> list_1.remove('t')
        >>> list_1 <= list_2
        True
        >>> list_2 <= list_1
        False
        """
        if self.__cmp__(other) != self.CMP_POSITIVE:
            return True
        return False

    def __hash__(self):
        """
        L.__hash__() <==> hash(L)

        >>> list_1 = List('test')
        >>> hash(list_1)
        1098142395
        """
        return hash(self.__repr__())

    def __getitem__(self, index):
        """
        L.__getitem__(index) <==> L[index]

        >>> list_1 = List('test')
        >>> list_1[0], list_1[1], list_1[2], list_1[3]
        ('t', 'e', 's', 't')
        >>> list_1[-1], list_1[-2], list_1[-3],list_1[-4]
        ('t', 's', 'e', 't')
        >>> list_1[10]
        Traceback (most recent call last):
            ...
        IndexError: List index out of range
        """
        return self._item(index)

    def __delitem__(self, index):
        """
        L.__delitem__(index) <==> del L[index]

        >>> list_1 = List('test')
        >>> del list_1[3]
        >>> list_1
        linkedlist.List(['t', 'e', 's'])
        """
        if not isinstance(index, int) and not isinstance(index, long):
            raise TypeError('List indices must be integers')

        if self.length == 0:
            raise IndexError('del from empty List')
        # Transform the negative intro a positive index
        if index < 0:
            index = self.length + index

        if index > self.length - 1 or index < 0:
            raise IndexError('List index out of range')

        if index == 0:
            self.head = self.head.link
            self.length -= self.step
            return

        previous = None
        current = self.head
        for _ in range(index):
            previous = current
            current = current.link
        previous.set_link(current.link)
        if current == self.tail:
            self.tail = previous
        self.length -= self.step

    def insert(self, index, value):
        """
        L.insert(index, value) -- insert value before index.

        >>> list_1 = List()
        >>> list_1.insert(1, 'test')
        >>> list_1.get()
        'test'
        >>> list_1.insert(0, 'spam')
        >>> list_1.get()
        'test'
        >>> list_1.head.value
        'spam'
        >>> list_1.insert(5, 'maps')
        >>> list_1.get()
        'maps'
        >>> list_1.insert(2, 333)
        >>> for item in list_1:  print(item)
        spam
        test
        333
        maps
        """
        # Transform the negative intro a positive index
        if index < 0:
            index = self.length + index
        # List index out of range
        if index > self.length:
            self.append(value)
            return
        # List has no items
        if self.length == 0:
            self.append(value)
            return
        # Insert item before one items
        if index == 0:
            self._appstart(value)
            return
        current = self.head
        # decrement the index because current position is set to
        # first item in the 'List'
        index -= self.step
        for _ in range(index):
            current = current.link
        node = _Node(value)
        node.set_link(current.link)
        current.set_link(node)
        self.length += self.step

    def remove(self, item):
        """
        L.remove(item) -- remove first occurrence item.
        Raises ValueError if item in not present.

        >>> list_1 = List('teslo')
        >>> list_1.remove('t')
        >>> list_1
        linkedlist.List(['e', 's', 'l', 'o'])
        >>> list_1.remove('o')
        >>> list_1
        linkedlist.List(['e', 's', 'l'])
        >>> list_1.remove('s')
        >>> list_1
        linkedlist.List(['e', 'l'])
        >>> list_1.remove('t')
        Traceback (most recent call last):
            ...
        ValueError: List.remove(x): x not in List
        """
        if self.length == 0:
            raise ValueError('List.remove(x): x not in List')
        if item == self.head.value:
            self.head = self.head.link
            self.length -= self.step
            return
        previous = None
        current = self.head
        while item != current.value:
            previous = current
            current = current.link
            if current is None:
                break
        if current is None:
            raise ValueError('List.remove(x): x not in List')
        previous.set_link(current.link)
        if current == self.tail:
            self.tail = previous
        self.length -= self.step

    def get(self):
        """
        L.get() -> item -- return the last item on the L.
        Raises ValueError if empty L.

        >>> list_1 = List('test')
        >>> list_1.get()
        't'
        >>> list_1.append('spam')
        >>> list_1.get()
        'spam'
        >>> list_2 = List()
        >>> list_2.get()
        Traceback (most recent call last):
            ...
        ValueError: get from empty List
        """
        if self.length == 0:
            raise ValueError('get from empty List')
        return self.tail.value

    def _item(self, index):
        """
        L.item(index) -> item -- returns the item found at index.
        Raises IndexError if item not found.
        Raises TypeError if index is not integers.
        >>> list_1 = List(['test', 'spam', 'maps'])
        >>> list_1._item(0)
        'test'
        >>> list_1._item(1)
        'spam'
        >>> list_1._item(10)
        Traceback (most recent call last):
            ...
        IndexError: List index out of range
        >>> list_1._item(-1)
        'maps'
        >>> list_1._item(-10)
        Traceback (most recent call last):
            ...
        IndexError: List index out of range
        >>> list_1._item('1')
        Traceback (most recent call last):
            ...
        TypeError: List indices must be integers
        """
        if not isinstance(index, int) and not isinstance(index, long):
            raise TypeError('List indices must be integers')
        if self.length == 0:
            raise IndexError('item from empty List')
        if index < 0:
            index = self.length + index
            # index += self.step
        if index == 0:
            return self.head.value
        if index > self.length - 1 or index < 0:
            raise IndexError('List index out of range')
        if index == self.length - 1:
            return self.tail.value
        current = self.head
        # decrement the index because current position is set to
        # first item in the 'List'
        # index -= self.step
        for _ in range(index):
            current = current.link
        return current.value

    def _appstart(self, element):
        """
        L._appstart(element) -- add element to start L.

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
            node = _Node(element)
            node.set_link(self.head)
            self.head = node
            self.length += self.step
        else:
            self.append(element)

    def append(self, element):
        """
        L.append(element) -- append element to end L.

        >>> list_1 = List('test')
        >>> list_1.tail.value
        't'
        >>> list_1.append('spam')
        >>> list_1.tail.value
        'spam'
        """
        if self.head is None:
            self.head = _Node(element)
            self.tail = self.head
        else:
            node = _Node(element)
            self.tail.set_link(node)
            self.tail = node
        self.length += self.step

    def extend(self, iterable):
        """
        L.extend(iterable) -- extend List by appending elements from
        the iterable.

        >>> list_1 = List(['test', 'spam'])
        >>> list_2 = List(['maps', 'food'])
        >>> list_1.extend(list_2)
        >>> list_1
        linkedlist.List(['test', 'spam', 'maps', 'food'])
        """
        if self is iterable:
            new = List(iterable)
        else:
            new = iterable

        for item in new:
            self.append(item)

    def pop(self, index=None):
        """
        L.pop(index) -> item -- remove and return item at
        index (default last) on the L.
        Raises IndexError if empty List.
        Raises TypeError if index is not integers.

        >>> list_1 = List('test')
        >>> list_1.append('spam')
        >>> list_1.append('maps')
        >>> list_1.tail.value
        'maps'
        >>> len(list_1)
        6
        >>> list_1.pop()
        maps
        >>> len(list_1)
        5
        >>> list_1.tail.value
        'spam'
        """
        if index is None:
            index = self.length - self.step

        if not isinstance(index, int) and not isinstance(index, long):
            raise TypeError('List indices must be integers')

        if self.length == 0:
            raise IndexError('pop from empty List')
        # Transform the negative intro a positive index
        if index < 0:
            index = self.length + index

        if index > self.length - 1 or index < 0:
            raise IndexError('List index out of range')

        if index == 0:
            node, self.head = self.head, self.head.link
            self.length -= self.step
            return node

        previous = None
        current = self.head
        for _ in range(index):
            previous = current
            current = current.link
        node = current
        previous.set_link(current.link)
        if current == self.tail:
            self.tail = previous
        self.length -= self.step
        return node


class _ListIter(object):
    """
    ListIter(obj) -> new ListIter initialized
    """

    current = None

    def __init__(self, obj):
        """
        LI.__init__(obj) -- initialized object ListIter

        >>> it = _ListIter(List('test'))
        >>> isinstance(it._current, _Node)
        True
        """
        self._current = obj.head

    def __iter__(self):
        """
        LI.__iter__() <==> iter(LI)

        >>> list_1 = List('test')
        >>> it = iter(list_1)
        >>> isinstance(it, _ListIter)
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
        if self._current is None:
            raise StopIteration
        note = self._current
        self._current = self._current.link
        return note.value


if __name__ == '__main__':
    import doctest
    doctest.testmod()
