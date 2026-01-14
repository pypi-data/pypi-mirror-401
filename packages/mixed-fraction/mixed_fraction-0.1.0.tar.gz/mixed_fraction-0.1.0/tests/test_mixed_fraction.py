from mixed_fraction import MixedFraction


def test_create_mixed_fraction():
    mf = MixedFraction(7, 3)
    assert mf is not None

import pytest
from mixed_fraction import MixedFraction


def test_exact_division_still_mixed():
    mf = MixedFraction(6, 3)
    s = str(mf)
    assert "—" in s  # still shown as mixed fraction


def test_negative_fraction():
    mf = MixedFraction(-7, 3)
    assert mf.to_fraction().numerator == -7


def test_addition():
    a = MixedFraction(1, 2)
    b = MixedFraction(1, 3)
    result = a + b
    assert result.to_fraction().numerator == 5
    assert result.to_fraction().denominator == 6


def test_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        MixedFraction(5, 0)
