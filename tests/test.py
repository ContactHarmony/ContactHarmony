import pytest

def decrement(x):
    return x-1

def test_example():
    assert decrement(4) == 2