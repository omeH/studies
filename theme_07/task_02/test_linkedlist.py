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
        # --- List->pop ---
        assert self.list_1.pop() == 333
        assert self.list_1.pop() == {}
        # --- List->__len__ ---
        assert len(self.list_1) == 2

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
        assert isinstance(self.it.next(), int)
        assert isinstance(self.it.next(), list)
        # --- ListIter->next->StopIteration ---
        with pytest.raises(StopIteration):
            self.it.next()
