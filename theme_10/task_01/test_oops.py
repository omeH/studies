import pytest

import oops


class TestOops(object):

    def setup_method(self, method):
        self.oops_i = oops.oops_indexerror
        self.oops_k = oops.oops_keyerror

    def test_used_oops(self):
        assert oops.main(self.oops_i) is None
        with pytest.raises(KeyError):
            oops.main(self.oops_k)
