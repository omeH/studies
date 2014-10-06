import pytest

import oops


class TestOops(object):

    def setup_method(self, method):
        self.oops_i = oops.oops_indexerror
        self.msg_i = oops.INDEXERROR_MESSAGE
        self.oops_o = oops.oops_oopserror
        self.msg_o = oops.OOPSERROR_MESAAGE

    def test_used_oops(self, capsys):
        oops.main(self.oops_i)
        out, err = capsys.readouterr()
        assert out == self.msg_i + '\n'

        oops.main(self.oops_o)
        out, err = capsys.readouterr()
        assert out == self.msg_o + '\n'
