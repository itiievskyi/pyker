import pytest
from pyker import Pyker
from pyker.config import BATCH_LIMIT


class TestBatching:
    pyker = Pyker()

    @pytest.mark.parametrize("batch_size, batch_limit", [(10, 5), (50, 3)])
    def test_batch_result(self, batch_size, batch_limit):
        assert self.pyker.random_digit() in range(0, 10)

        # if `batch` is valid, the return value is always of list type
        assert type(self.pyker.random_digit(batch=True)) == list

        # BATCH_LIMIT is a default value
        assert len(self.pyker.random_digit(batch=True)) <= BATCH_LIMIT

        # the list should have an exact size if appropriate value is passed
        assert len(self.pyker.random_digit(batch=batch_size)) == batch_size

        # setting batch limit globally, so the every random batch will use it as upper limit
        self.pyker.set_batch_limit(batch_limit)
        assert len(self.pyker.random_digit(batch=True)) <= batch_limit
