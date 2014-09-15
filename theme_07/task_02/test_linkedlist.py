import pytest

import linkedlist as ll


class TestClass(object):

    def setup_method(self, method):
        # linkedlist.Node
        self.node_1 = ll._Node('test')
        self.node_2 = ll._Node('spam')
        # linkedlist.List
        self.CMP_NEGATIVE = -1
        self.CMP_ZERO = 0
        self.CMP_POSITIVE = 1
        self.test_list = ['t', 'e', 's', 't']
        self.test_dict = {1: None, 2: None, 3: None, 4: None}
        self.test_tuple = (1, 2, 3, 4)
        self.items = ['test', 'spam', 'maps', 'food']
        self.list_1 = ll.List(self.items)
        self.item = 333
        self.list_2 = ll.List([self.item])
        self.list_3 = ll.List()
        # linkedlist.List
        self.it_1 = iter(self.list_1)
        self.it_2 = iter(self.list_3)

    ###################################
    # Tests for class linkedlist.Node #
    ###################################

    def test_node_init(self):
        assert self.node_1.value == 'test'
        assert self.node_1.link is None

    def test_node_str(self):
        assert self.node_1.__str__() == 'test'
        assert self.node_2.__str__() == 'spam'
        # <<<<<>>>>> #
        assert str(self.node_1) == 'test'
        assert str(self.node_2) == 'spam'

    def test_node_repr(self):
        assert self.node_1.__repr__() == 'test'
        assert self.node_2.__repr__() == 'spam'
        # <<<<<>>>>> #
        assert repr(self.node_1) == 'test'
        assert repr(self.node_2) == 'spam'

    def test_node_set_link(self):
        self.node_1.set_link(self.node_2)
        assert self.node_1.link == self.node_2
        # ---------- #
        self.node_2.set_link(self.node_1)
        assert self.node_2.link == self.node_1

    ###################################
    # Tests for class linkedlist.List #
    ###################################

    def test_list_init(self):
        assert self.list_1.head.value == 'test'
        assert self.list_1.tail.value == 'food'
        assert self.list_1.length == len(self.items)
        assert self.list_1.head.link is not None
        assert self.list_1.tail.link is None
        # ---------- #
        assert self.list_2.head.value == self.item
        assert self.list_2.tail.value == self.item
        assert self.list_2.length == 1
        assert self.list_2.head.link is None
        assert self.list_2.tail.link is None
        # ---------- #
        assert self.list_3.head is None
        assert self.list_3.tail is None
        assert self.list_3.length == 0
        # ---------- #
        list_4 = ll.List(self.list_1)
        assert list_4.head.value == 'test'
        assert list_4.tail.value == 'food'
        assert list_4.length == len(self.items)
        assert list_4.head.link is not None
        assert list_4.tail.link is None
        # ---------- #
        list_5 = ll.List(tuple(self.items))
        assert list_5.head.value == 'test'
        assert list_5.tail.value == 'food'
        assert list_5.length == len(self.items)
        assert list_5.head.link is not None
        assert list_5.tail.link is None
        # ---------- #
        items = {'test': None, 'spam': None, 'maps': None, 'food': None}
        list_6 = ll.List(items)
        assert 'test' in list_6
        assert 'food' in list_6
        assert 'spam' in list_6
        assert 'maps' in list_6
        assert list_6.length == len(items)
        assert list_6.head.link is not None
        assert list_6.tail.link is None

    def test_list_len(self):
        assert self.list_1.__len__() == len(self.items)
        assert self.list_2.__len__() == 1
        assert self.list_3.__len__() == 0
        # <<<<<>>>>> #
        assert len(self.list_1) == len(self.items)
        assert len(self.list_2) == 1
        assert len(self.list_3) == 0

    def test_list_iter(self):
        assert isinstance(self.list_1.__iter__(), ll._ListIter)
        assert isinstance(self.list_2.__iter__(), ll._ListIter)
        assert isinstance(self.list_3.__iter__(), ll._ListIter)
        # <<<<<>>>>> #
        assert isinstance(iter(self.list_1), ll._ListIter)
        assert isinstance(iter(self.list_2), ll._ListIter)
        assert isinstance(iter(self.list_3), ll._ListIter)

    def test_list_str(self):
        assert self.list_1.__str__() == str(self.items)
        assert self.list_2.__str__() == str([self.item])
        assert self.list_3.__str__() == str([])
        # <<<<<>>>>> #
        assert str(self.list_1) == str(self.items)
        assert str(self.list_2) == str([self.item])
        assert str(self.list_3) == str([])

    def test_list_repr(self):
        str_1 = 'linkedlist.List({0})'.format(self.items)
        str_2 = 'linkedlist.List([{0}])'.format(self.item)
        str_3 = 'linkedlist.List([])'
        # <<<<<>>>>> #
        assert self.list_1.__repr__() == str_1
        assert self.list_2.__repr__() == str_2
        assert self.list_3.__repr__() == str_3
        # <<<<<>>>>> #
        assert repr(self.list_1) == str_1
        assert repr(self.list_2) == str_2
        assert repr(self.list_3) == str_3

    def test_list_add(self):
        list_4 = self.list_1.__add__(self.list_1)
        assert list_4.__getitem__(4) == 'test'
        assert list_4.__getitem__(7) == 'food'
        assert len(list_4) == len(self.list_1) + len(self.list_1)
        # ---------- #
        list_5 = self.list_2.__add__(self.list_2)
        assert list_5.__getitem__(0) == self.item
        assert list_5.__getitem__(1) == self.item
        assert len(list_5) == 2
        # ---------- #
        list_6 = self.list_3.__add__(self.list_3)
        with pytest.raises(IndexError):
            list_6.__getitem__(0)
        assert len(list_6) == 0
        # ---------- #
        with pytest.raises(TypeError):
            self.list_1.__add__('test')
        # <<<<<>>>>> #
        list_4 = self.list_1 + self.list_1
        assert list_4.__getitem__(4) == 'test'
        assert list_4.__getitem__(7) == 'food'
        assert len(list_4) == len(self.list_1) + len(self.list_1)
        # ---------- #
        list_5 = self.list_2 + self.list_2
        assert list_5.__getitem__(0) == self.item
        assert list_5.__getitem__(1) == self.item
        assert len(list_5) == 2
        # ---------- #
        list_6 = self.list_3 + self.list_3
        with pytest.raises(IndexError):
            list_6.__getitem__(0)
        assert len(list_6) == 0
        # ---------- #
        with pytest.raises(TypeError):
            self.list_1 + 'test'

    def test_list_iadd(self):
        list_4 = ll.List(self.list_1)
        list_4.__iadd__(list_4)
        assert list_4.__getitem__(4) == 'test'
        assert list_4.__getitem__(7) == 'food'
        assert len(list_4) == len(self.items) + len(self.items)
        # ---------- #
        list_5 = ll.List(self.list_2)
        list_5.__iadd__(list_5)
        assert list_5.__getitem__(0) == self.item
        assert list_5.__getitem__(1) == self.item
        assert len(list_5) == 2
        # ---------- #
        list_6 = ll.List(self.list_3)
        list_6.__iadd__(list_6)
        with pytest.raises(IndexError):
            list_6.__getitem__(0)
        assert len(list_6) == 0
        # ---------- #
        list_4 = ll.List(self.list_1)
        list_4.__iadd__('teslo')
        assert list_4.__getitem__(4) == 't'
        assert list_4.__getitem__(8) == 'o'
        assert len(list_4) == len(self.items) + len('teslo')
        # ---------- #
        items = {'teslo': None, 'log': None, 'step': None, 'info': None}
        list_4 = ll.List(self.list_1)
        list_4.__iadd__(items)
        assert 'teslo' in list_4
        assert 'log' in list_4
        assert 'step' in list_4
        assert 'info' in list_4
        assert len(list_4) == len(self.items) + len(items)
        # ---------- #
        list_4 = ll.List(self.list_1)
        with pytest.raises(TypeError):
            list_4.__iadd__(333)

    def test_list_cmp(self):
        assert self.list_1.__cmp__(self.list_1) == self.CMP_ZERO
        assert self.list_1.__cmp__(self.list_2) == self.CMP_POSITIVE
        assert self.list_2.__cmp__(self.list_1) == self.CMP_NEGATIVE
        assert self.list_1.__cmp__(self.list_3) == self.CMP_POSITIVE
        assert self.list_3.__cmp__(self.list_1) == self.CMP_NEGATIVE
        # ---------- #
        items = [1, 2, 3, 4]
        list_4 = ll.List(items)
        list_5 = ll.List(items[:-1])
        assert list_4.__cmp__(list_5) == self.CMP_POSITIVE
        assert list_5.__cmp__(list_4) == self.CMP_NEGATIVE
        # ---------- #
        list_5 = ll.List(items)
        assert list_4.__cmp__(list_5) == self.CMP_ZERO
        # ---------- #
        items.reverse()
        list_5 = ll.List(items)
        assert list_4.__cmp__(list_5) == self.CMP_NEGATIVE
        # ---------- #
        assert list_4.__cmp__('test') == self.CMP_NEGATIVE

    def test_list_eq(self):
        assert self.list_1.__eq__(ll.List(self.items)) is True
        assert self.list_1.__eq__(ll.List([self.item])) is False
        # ---------- #
        assert self.list_2.__eq__(ll.List([self.item])) is True
        assert self.list_2.__eq__(ll.List(self.items)) is False
        # ---------- #
        assert self.list_3.__eq__(ll.List()) is True
        assert self.list_3.__eq__(ll.List([self.item])) is False
        # <<<<<>>>>> #
        assert (self.list_1 == ll.List(self.items)) is True
        assert (self.list_1 == ll.List([self.item])) is False
        # ---------- #
        assert (self.list_2 == ll.List([self.item])) is True
        assert (self.list_2 == ll.List(self.items)) is False
        # ---------- #
        assert (self.list_3 == ll.List()) is True
        assert (self.list_3 == ll.List([self.item])) is False

    def test_list_ne(self):
        assert self.list_1.__ne__(ll.List([self.item])) is True
        assert self.list_1.__ne__(ll.List(self.items)) is False
        # ---------- #
        assert self.list_2.__ne__(ll.List(self.items)) is True
        assert self.list_2.__ne__(ll.List([self.item])) is False
        # ---------- #
        assert self.list_3.__ne__(ll.List([self.item])) is True
        assert self.list_3.__ne__(ll.List()) is False
        # <<<<<>>>>> #
        assert (self.list_1 != ll.List([self.item])) is True
        assert (self.list_1 != ll.List(self.items)) is False
        # ---------- #
        assert (self.list_2 != ll.List(self.items)) is True
        assert (self.list_2 != ll.List([self.item])) is False
        # ---------- #
        assert (self.list_3 != ll.List([self.item])) is True
        assert (self.list_3 != ll.List()) is False

    def test_list_gt(self):
        assert self.list_1.__gt__(ll.List([self.item])) is True
        assert self.list_1.__gt__(ll.List(self.items)) is False
        # ---------- #
        assert self.list_2.__gt__(ll.List()) is True
        assert self.list_2.__gt__(ll.List([self.item])) is False
        # ---------- #
        assert self.list_3.__gt__(ll.List()) is False
        # <<<<<>>>>> #
        assert (self.list_1 > ll.List([self.item])) is True
        assert (self.list_1 > ll.List(self.items)) is False
        # ---------- #
        assert (self.list_2 > ll.List()) is True
        assert (self.list_2 > ll.List([self.item])) is False
        # ---------- #
        assert (self.list_3 > ll.List()) is False

    def test_list_lt(self):
        assert self.list_1.__lt__(ll.List([self.item])) is False
        assert self.list_1.__lt__(ll.List(self.items * 2)) is True
        # ---------- #
        assert self.list_2.__lt__(ll.List(self.items)) is True
        assert self.list_2.__lt__(ll.List([self.item])) is False
        # ---------- #
        assert self.list_3.__lt__(ll.List([self.item])) is True
        assert self.list_3.__lt__(ll.List()) is False
        # <<<<<>>>>> #
        assert (self.list_1 < ll.List([self.item])) is False
        assert (self.list_1 < ll.List(self.items * 2)) is True
        # ---------- #
        assert (self.list_2 < ll.List(self.items)) is True
        assert (self.list_2 < ll.List([self.item])) is False
        # ---------- #
        assert (self.list_3 < ll.List([self.item])) is True
        assert (self.list_3 < ll.List()) is False

    def test_list_ge(self):
        assert self.list_1.__ge__(ll.List([self.item])) is True
        assert self.list_1.__ge__(ll.List(self.items)) is True
        assert self.list_1.__ge__(ll.List(self.items * 2)) is False
        # ---------- #
        assert self.list_2.__ge__(ll.List(self.items)) is False
        assert self.list_2.__ge__(ll.List([self.item])) is True
        assert self.list_2.__ge__(ll.List()) is True
        # ---------- #
        assert self.list_3.__ge__(ll.List([self.item])) is False
        assert self.list_3.__ge__(ll.List()) is True
        # <<<<<>>>>> #
        assert (self.list_1 >= ll.List([self.item])) is True
        assert (self.list_1 >= ll.List(self.items)) is True
        assert (self.list_1 >= ll.List(self.items * 2)) is False
        # ---------- #
        assert (self.list_2 >= ll.List(self.items)) is False
        assert (self.list_2 >= ll.List([self.item])) is True
        assert (self.list_2 >= ll.List()) is True
        # ---------- #
        assert (self.list_3 >= ll.List([self.item])) is False
        assert (self.list_3 >= ll.List()) is True

    def test_list_le(self):
        assert self.list_1.__le__(ll.List([self.item])) is False
        assert self.list_1.__le__(ll.List(self.items)) is True
        assert self.list_1.__le__(ll.List(self.items * 2)) is True
        # ---------- #
        assert self.list_2.__le__(ll.List(self.items)) is True
        assert self.list_2.__le__(ll.List([self.item])) is True
        assert self.list_2.__le__(ll.List()) is False
        # ---------- #
        assert self.list_3.__le__(ll.List([self.item])) is True
        assert self.list_3.__le__(ll.List()) is True
        # <<<<<>>>>> #
        assert (self.list_1 <= ll.List([self.item])) is False
        assert (self.list_1 <= ll.List(self.items)) is True
        assert (self.list_1 <= ll.List(self.items * 2)) is True
        # ---------- #
        assert (self.list_2 <= ll.List(self.items)) is True
        assert (self.list_2 <= ll.List([self.item])) is True
        assert (self.list_2 <= ll.List()) is False
        # ---------- #
        assert (self.list_3 <= ll.List([self.item])) is True
        assert (self.list_3 <= ll.List()) is True

    def test_list_getitem(self):
        assert self.list_1[0] == 'test'
        assert self.list_1[1] == 'spam'
        assert self.list_1[2] == 'maps'
        assert self.list_1[3] == 'food'
        with pytest.raises(IndexError):
            self.list_1[4]
        with pytest.raises(TypeError):
            self.list_1['1']
        # ---------- #
        assert self.list_1[-1] == 'food'
        assert self.list_1[-2] == 'maps'
        assert self.list_1[-3] == 'spam'
        assert self.list_1[-4] == 'test'
        with pytest.raises(IndexError):
            self.list_1[-5]

    def test_list_delitem(self):
        list_tmp = ll.List(self.list_1)
        items_tmp = self.items[:]
        # <<<<<>>>>> #
        list_tmp.__delitem__(0)
        items_tmp.remove('test')
        assert len(list_tmp) == len(items_tmp)
        assert ('test' in list_tmp) is False
        # ---------- #
        list_tmp.__delitem__(1)
        items_tmp.remove('maps')
        assert len(list_tmp) == len(items_tmp)
        assert ('maps' in list_tmp) is False
        # ---------- #
        list_tmp.__delitem__(1)
        items_tmp.remove('food')
        assert len(list_tmp) == len(items_tmp)
        assert ('food' in list_tmp) is False
        # ---------- #
        with pytest.raises(IndexError):
            list_tmp.__delitem__(1)
        # ---------- #
        with pytest.raises(TypeError):
            list_tmp.__delitem__('1')
        # ---------- #
        list_tmp.__delitem__(0)
        items_tmp.remove('spam')
        assert len(list_tmp) == len(items_tmp)
        assert ('spam' in list_tmp) is False
        # ---------- #
        with pytest.raises(IndexError):
            list_tmp.__delitem__(1)
        # <<<<<>>>>> #
        list_tmp = ll.List(self.list_1)
        items_tmp = self.items[:]
        # <<<<<>>>>> #
        list_tmp.__delitem__(-4)
        items_tmp.remove('test')
        assert len(list_tmp) == len(items_tmp)
        assert ('test' in list_tmp) is False
        # ---------- #
        list_tmp.__delitem__(-2)
        items_tmp.remove('maps')
        assert len(list_tmp) == len(items_tmp)
        assert ('maps' in list_tmp) is False
        # ---------- #
        list_tmp.__delitem__(-1)
        items_tmp.remove('food')
        assert len(list_tmp) == len(items_tmp)
        assert ('food' in list_tmp) is False
        # ---------- #
        with pytest.raises(IndexError):
            list_tmp.__delitem__(-2)

    def test_list_insert(self):
        self.list_1.insert(0, 'm1')
        assert self.list_1[0] == 'm1'
        self.list_1.insert(1, 'm2')
        assert self.list_1[1] == 'm2'
        self.list_1.insert(10, 'm3')
        assert self.list_1.get() == 'm3'
        # ---------- #
        self.list_1.insert(-1, 'm4')
        assert self.list_1[-2] == 'm4'
        self.list_1.insert(-8, 'm5')
        assert self.list_1[-9] == 'm5'
        self.list_1.insert(-15, 'm6')
        assert self.list_1[-10] == 'm6'

    def test_list_remove(self):
        assert len(self.list_1) == len(self.items)
        self.list_1.remove('test')
        assert ('test' in self.list_1) is False
        assert len(self.list_1) == len(self.items) - 1
        self.list_1.remove('maps')
        assert ('maps' in self.list_1) is False
        assert len(self.list_1) == len(self.items) - 2
        self.list_1.remove('food')
        assert('food' in self.list_1) is False
        assert len(self.list_1) == len(self.items) - 3
        with pytest.raises(ValueError):
            self.list_1.remove('list')
        # ---------- #
        with pytest.raises(ValueError):
            self.list_3.remove('test')

    def test_list_item(self):
        self.test_list_getitem()

    def test_list_appstart(self):
        assert len(self.list_1) == len(self.items)
        self.list_1._appstart('list')
        assert len(self.list_1) == len(self.items) + 1
        assert self.list_1[0] == 'list'
        # ---------- #
        assert len(self.list_3) == 0
        self.list_3._appstart('list')
        assert len(self.list_3) == 1
        assert self.list_3[0] == 'list'

    def test_list_get(self):
        assert self.list_1.get() == self.items[-1]
        self.list_1.append('list')
        assert self.list_1.get() == 'list'
        # ---------- #
        with pytest.raises(ValueError):
            self.list_3.get()

    def test_list_append(self):
        assert self.list_1.get() == self.items[-1]
        self.list_1.append('list')
        assert self.list_1.get() == 'list'
        # ---------- #
        with pytest.raises(ValueError):
            self.list_3.get()
        self.list_3.append('list')
        assert self.list_3.get() == 'list'

    def test_list_extend(self):
        self.list_1.extend(self.test_list)
        assert len(self.list_1) == len(self.items) + len(self.test_list)
        # ---------- #
        self.list_2.extend(self.test_dict)
        assert len(self.list_2) == 1 + len(self.test_dict)
        # ---------- #
        self.list_3.extend(self.test_tuple)
        assert len(self.list_3) == len(self.test_tuple)
        # ---------- #
        self.list_1.extend(self.list_3)
        assert len(self.list_1) == \
            len(self.items) + len(self.test_list) + len(self.test_tuple)

    def test_list_pop(self):
        self.list_1.extend(self.test_list)
        assert self.list_1.pop(0) == self.items[0]
        assert self.list_1.pop(2) == self.items[-1]
        assert self.list_1.pop() == self.test_list[-1]
        # ---------- #
        assert self.list_1.pop(-1) == self.test_list[-2]
        assert self.list_1.pop(-2) == self.test_list[0]
        # ---------- #
        with pytest.raises(IndexError):
            self.list_1.pop(10)
        # ---------- #
        with pytest.raises(TypeError):
            self.list_1.pop('spam')
        # ---------- #
        with pytest.raises(IndexError):
            self.list_3.pop()

    def test_listiter(self):
        self.list_1 = ll.List('test')
        self.list_1.append(333)
        self.list_1.append([])
        # --- List->__iter__ ---
        # --- ListIter->__init__ ---
        self.it = iter(self.list_1)
        assert isinstance(self.it, ll._ListIter)
        # --- ListIter->next ---
        assert isinstance(self.it.next(), str)
        assert isinstance(self.it.next(), str)
        assert isinstance(self.it.next(), str)
        assert isinstance(self.it.next(), str)
        assert isinstance(self.it.next(), int)
        assert isinstance(self.it.next(), list)
        # --- ListIter->next->StopIteration ---
        with pytest.raises(StopIteration):
            self.it.next()

    #######################################
    # Tests for class linkedlist.ListIter #
    #######################################

    def test_listiter_init(self):
        assert self.it_1._current == self.list_1.head
        assert self.it_2._current == self.list_3.head

    def test_listiter_iter(self):
        assert isinstance(self.it_1.__iter__(), ll._ListIter)
        assert isinstance(iter(self.it_2), ll._ListIter)

    def test_listiter_next(self):
        for index in range(len(self.list_1)):
            if self.it_1.next() != self.items[index]:
                pytest.fail('Bad _ListIter.next()')
        # ---------- #
        with pytest.raises(StopIteration):
            self.it_2.next()
