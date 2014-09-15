import os
import copy

import pytest

import linkedlist as ll

if "TEST_PYTHON_LIST" in os.environ:
    List = list
else:
    List = ll.List


class TestListInterface(object):
    TEST_TUPLE = (1, 2, 3)
    TEST_LIST = [1, 2, 3]
    REVERSED_TEST_LIST = [3, 2, 1]
    TEST_DICT = {1: None, 2: None, 3: None}
    TEST_STR = '123'
    TEST_STR_AS_LIST = ['1', '2', '3']
    TEST_LEN = 3
    TEST_100500 = 100500

    def test_list_init(self):
        l = List( self.TEST_TUPLE )
        assert len(l) == self.TEST_LEN
        assert [elem for elem in l] == self.TEST_LIST

        l = List( self.TEST_LIST )
        assert len(l) == self.TEST_LEN
        assert [elem for elem in l] == self.TEST_LIST

        l = List( self.TEST_DICT )
        assert len(l) == self.TEST_LEN
        assert [elem for elem in l] == self.TEST_LIST

        l = List( self.TEST_TUPLE )
        l2 = List(l)
        assert len(l2) == self.TEST_LEN
        assert [elem for elem in l2] == self.TEST_LIST

        l = List(self.TEST_STR)
        assert len(l) == self.TEST_LEN
        assert [elem for elem in l] == self.TEST_STR_AS_LIST

        with pytest.raises(TypeError):
            l = List(self.TEST_100500)

        l = List()
        for elem in self.TEST_TUPLE:
            l.append(elem)
        assert len(l) == self.TEST_LEN
        assert [elem for elem in l] == self.TEST_LIST

    def test_list_add(self):
        l1 = List( self.TEST_TUPLE )
        l2 = List( self.TEST_TUPLE )
        assert [elem for elem in l1 + l2] == self.TEST_LIST + self.TEST_LIST

        assert len(l1) == self.TEST_LEN
        assert [elem for elem in l1] == self.TEST_LIST
        assert len(l2) == self.TEST_LEN
        assert [elem for elem in l2] == self.TEST_LIST

        l1 = List( self.TEST_TUPLE )
        l2 = List( self.TEST_TUPLE )
        l1 += l2
        assert len(l1) == self.TEST_LEN * 2
        assert [elem for elem in l1] == self.TEST_LIST + self.TEST_LIST

        assert len(l2) == self.TEST_LEN
        assert [elem for elem in l2] == self.TEST_LIST

    def test_corner_cases(self):
        l = List([self.TEST_100500])
        assert len(l) == 1
        assert l[0] == self.TEST_100500

        l = List()
        assert len(l) == 0

        l = List()
        l.append(l)

        # some buggy containers generate runtime errors here:)
        # RuntimeError: maximum recursion depth exceeded while calling a Python object
        # with pytest.raises(RuntimeError):
        assert str(l) == '[[...]]'

        l1 = List()
        l2 = List()
        l2.append(l1)
        l1.append(l2)
        assert str(l1) == '[[...]]'
        assert str(l2) == '[[...]]'

    def test_copy(self):
        l1 = List( self.TEST_LIST )
        l2 = copy.copy(l1)
        for elem in l1:
            if elem not in l2:
                pytest.fail("Invalid copy l1 to l2")

    def test_equality(self):
        l1 = List( self.TEST_LIST )
        l2 = List( self.TEST_TUPLE )
        assert l1 == l2

        class A(object):
            pass

        a1 = A()
        a2 = A()

        l1 = List( (a1, a2) )
        l2 = List( (a1, a2) )
        assert l1 == l2

        l1 = List( (a1, a2) )
        l2 = List( (a2, a1) )
        assert l1 != l2

        l1 = List()
        l2 = List(self.TEST_STR)
        assert l1 != l2

        class B(object):
            def __cmp__(self, x):
                return 0

        b1 = B()
        b2 = B()
        l1 = List( (b1, b2) )
        l2 = List( (b2, b1) )
        assert l1 == l2

        l1 = List( self.TEST_LIST )
        l2 = List( [1] )
        assert l1 != l2
        assert l1 > l2
        assert l1 >= l2
        assert l2 <= l1

    def test_indexing(self):
        l1 = List( self.TEST_LIST )
        assert l1[0] == 1
        assert l1[1] == 2
        assert l1[2] == 3
        with pytest.raises(IndexError):
            l1[3]
        assert l1[-1] == 3
        assert l1[-2] == 2
        assert l1[-3] == 1
        with pytest.raises(IndexError):
            l1[-4]

        with pytest.raises(TypeError):
            l1['a']

    def test_pop(self):
        l1 = List( self.TEST_LIST )
        assert l1.pop() == 3
        assert len(l1) == 2

        assert l1.pop() == 2
        assert len(l1) == 1

        assert l1.pop() == 1
        assert len(l1) == 0

        with pytest.raises(IndexError):
            l1.pop()
        assert len(l1) == 0

        l1 = List( self.TEST_LIST )
        assert l1.pop(0) == 1
        assert len(l1) == 2
        assert l1.pop(0) == 2
        assert len(l1) == 1
        assert l1.pop(0) == 3
        assert len(l1) == 0
        with pytest.raises(IndexError):
            l1.pop()
        assert len(l1) == 0

        l1 = List( self.TEST_LIST )
        assert l1.pop(-2) == 2
        assert len(l1) == 2

        l1 = List( self.TEST_LIST )
        with pytest.raises(IndexError):
            l1.pop(-5)

    def test_extend(self):
        l1 = List( self.TEST_LIST )
        l1.extend( self.TEST_TUPLE )
        assert len(l1) == 2 * self.TEST_LEN
        assert [elem for elem in l1] == 2 * self.TEST_LIST

        l1.extend( l1 )
        assert len(l1) == 4 * self.TEST_LEN
        assert [elem for elem in l1] == 4 * self.TEST_LIST

    def test_append(self):
        l1 = List()
        for _ in range( self.TEST_LEN ):
            l1.append( self.TEST_TUPLE )

        assert len(l1) == self.TEST_LEN
        assert [elem for elem in l1] == [self.TEST_TUPLE] * self.TEST_LEN

    def test_insert(self):
        l1 = List( self.TEST_LIST )
        for elem in self.TEST_TUPLE:
            l1.insert(0, elem)

        assert len(l1) == self.TEST_LEN * 2
        assert [elem for elem in l1] == self.REVERSED_TEST_LIST + self.TEST_LIST

        l1 = List( self.TEST_LIST )
        for elem in self.TEST_TUPLE:
            l1.insert(-1, elem)

        assert len(l1) == self.TEST_LEN * 2
        assert [elem for elem in l1] == [1, 2, 1, 2, 3, 3]

        l1 = List( self.TEST_LIST )
        for elem in self.TEST_TUPLE:
            l1.insert(1, elem)

        assert len(l1) == self.TEST_LEN * 2
        assert [elem for elem in l1] == [1, 3, 2, 1, 2, 3]

    def test_remove(self):
        l1 = List( self.TEST_LIST )
        l1.remove(2)
        assert len(l1) == self.TEST_LEN - 1
        assert [elem for elem in l1] == [1, 3]

        l1 = List( self.TEST_LIST )
        l1.remove(3)
        assert len(l1) == self.TEST_LEN - 1
        assert [elem for elem in l1] == [1, 2]

        l1 = List( self.TEST_LIST * 2 )
        l1.remove(3)
        assert len(l1) == self.TEST_LEN * 2 - 1
        assert [elem for elem in l1] == [1, 2, 1, 2, 3]

        l1 = List( self.TEST_LIST )
        for elem in self.TEST_LIST:
            l1.remove(elem)
        assert len(l1) == 0
        with pytest.raises(ValueError):
            l1.remove(0)

    def test_del(self):
        l1 = List( self.TEST_LIST )
        del l1[0]
        assert len(l1) == self.TEST_LEN - 1
        assert [elem for elem in l1] == [2, 3]

        l1 = List( self.TEST_LIST )
        with pytest.raises(IndexError):
            del l1[self.TEST_100500]
