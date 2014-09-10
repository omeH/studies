import pytest

import linkedlist as ll


class TestClass(object):

    def test_node(self):
        self.node_1 = ll.Node('test')
        # --- Node->__init__ ---
        assert isinstance(self.node_1, ll.Node)
        assert self.node_1.value == 'test'
        # --- Node->__str__ ---
        assert str(self.node_1) == 'test'
        self.node_2 = ll.Node('spam')
        self.node_1.set_link(self.node_2)
        self.node_2.set_link(self.node_1)
        # --- Node->set_link ---
        assert self.node_1.link is self.node_2
        assert self.node_2.link is self.node_1

    def test_list(self):
        self.list_1 = ll.List()
        # --- List->__init__(value=None) ---
        assert self.list_1.head is None
        assert self.list_1.tail is None
        self.list_1 = ll.List([])
        # --- List->__init__(value) ---
        # --- List->get ---
        # assert isinstance(self.list_1.get(), None)
        assert self.list_1.get() is None
        self.list_1 = ll.List([[]])
        assert isinstance(self.list_1.get(), list)
        assert self.list_1.get() == []
        # --- List->append ---
        self.list_1.append('test')
        assert isinstance(self.list_1.get(), str)
        assert self.list_1.get() == 'test'
        # --- List->append ---
        self.list_1.append({})
        assert isinstance(self.list_1.get(), dict)
        assert self.list_1.get() == {}
        # --- List->append ---
        self.list_1.append(333)
        assert isinstance(self.list_1.get(), int)
        assert self.list_1.get() == 333
        # --- List->appstart ---
        self.list_1._appstart(222)
        assert self.list_1.head.value == 222
        self.list_1._appstart('maps')
        assert self.list_1.head.value == 'maps'
        # --- List->insert ---
        self.list_1.insert(3, 'spam')
        self.list_1.insert(0, 'flood')
        assert self.list_1.head.value == 'flood'
        self.list_1.insert(10, 'food')
        assert self.list_1.get() == 'food'
        assert len(self.list_1) == 9
        # --- List->pop ---
        assert self.list_1.pop() == 'food'
        assert self.list_1.pop() == 333
        # --- List->__len__ ---
        assert len(self.list_1) == 7
        self.list_2 = ll.List(['test'])
        self.list_3 = ll.List(['test'])
        assert self.list_2 == self.list_3
        assert self.list_1 != self.list_2

    def test_list_insert(self):
        self.list_1 = ll.List(['test', 'spam', 'maps', 'food'])
        self.list_1.insert(0, 'm1')
        assert self.list_1.head.value == 'm1'
        self.list_1.insert(1, 'm2')
        assert self.list_1.head.value == 'm2'
        self.list_1.insert(2, 'm3')
        assert self.list_1.head.link.value == 'm3'
        self.list_1.insert(10, 'm4')
        assert self.list_1.get() == 'm4'
        self.list_1.insert(-1, 'm5')
        current = self.list_1.head
        while current.link != self.list_1.tail:
            current = current.link
        assert current.value == 'm5'
        self.list_1.insert(-9, 'm6')
        assert self.list_1.head.value == 'm6'

    def test_listiter(self):
        self.list_1 = ll.List('test')
        self.list_1.append(333)
        self.list_1.append([])
        # --- List->__iter__ ---
        # --- ListIter->__init__ ---
        self.it = iter(self.list_1)
        assert isinstance(self.it, ll.ListIter)
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
