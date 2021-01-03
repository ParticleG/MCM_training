import numpy as np

from decimal import Decimal as Dec


def _calculate_expectation(_total_count, _infect_rate, _group_size):
    _successive_multiplication = Dec(1)
    for _iterator in np.arange(0, int(_group_size) + 1):
        _successive_multiplication *= ((Dec(1) - _infect_rate) * _total_count - Dec(int(_iterator))) / (
                _total_count - Dec(int(_iterator)))
    return _successive_multiplication * _group_size


def calculate_group_size(_total_count, _infect_rate, _minimum, _maximum):
    _middle = Dec(_minimum + _maximum) / Dec(2)
    _middle_middle = Dec(_minimum + _middle) / Dec(2)
    _middle_expectation = _calculate_expectation(_total_count, _infect_rate, _middle)
    _middle_middle_expectation = _calculate_expectation(_total_count, _infect_rate, _middle_middle)
    if np.abs(_middle - _middle_middle) < 0.001:
        return _middle, _middle_expectation
    if _middle_expectation > _middle_middle_expectation:
        _result = calculate_group_size(_total_count, _infect_rate, _middle_middle, _maximum)
    else:
        _result = calculate_group_size(_total_count, _infect_rate, _minimum, _middle)
    return _result


if __name__ == "__main__":
    total_count = 1
    infect_rate = Dec('0.05')
    if total_count > 10000:
        check_limit = Dec(10000)
    else:
        check_limit = Dec(total_count)
    group_size, negative_expectation = calculate_group_size(total_count, infect_rate, 0, check_limit)
    print(f"group_size: {group_size}, "
          f"negative_expectation: {negative_expectation}, "
          f"negative_rate: {negative_expectation / group_size}, ")
