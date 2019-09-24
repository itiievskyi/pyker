import pytest
from pyker import Pyker
from pyker.config import BATCH_LIMIT


class TestBatching:
    pyker = Pyker()

    @pytest.mark.parametrize(
        "batch_size, batch_limit, batch_limits", [(10, 5, (100, 105)), (50, 3, (5, 10))]
    )
    def test_batch_result(self, batch_size, batch_limit, batch_limits):
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

        # providing start and end limits explicitly
        length = len(self.pyker.random_digit(batch=batch_limits))
        assert length >= batch_limits[0] and length < batch_limits[1]
