from calculate_group_size import *


def check_disease(_total_population, _infection_rate, previous_group_size,
                  _false_negative_rate, _false_positive_rate, _recessive_rate):  # b,a,beta
    _next_population, _negative_expect = calculate_group_size(_total_population, _infection_rate, previous_group_size)
    _check_counts = np.ceil(_total_population / _next_population) + np.round(  # Original negative groups
        _total_population / _next_population * (_negative_expect / _next_population) * (
                1 +  # First check
                (1 - _false_positive_rate) * (1 - _false_negative_rate) * (1 - _recessive_rate) +  # Truly negative groups, considered false positives
                _false_negative_rate * ((1 - _false_negative_rate) * _recessive_rate + _false_negative_rate)  # False negatives in positive groups
        )
    )
    _positive_group_count = np.round(
        _total_population / _next_population * (1 - _negative_expect / _next_population) +  # Original positive groups
        _false_positive_rate * (1 - _false_negative_rate) * (1 - _recessive_rate) +  # False positives in negative groups
        (1 - _false_negative_rate) * ((1 - _false_negative_rate) * _recessive_rate + _false_negative_rate)  # Positive groups in second check
    )
    _next_infection_rate = _infection_rate / (1 - _false_positive_rate) * (1 - _false_negative_rate) * (1 - _recessive_rate)
    return _next_population, _next_infection_rate, _check_counts, _positive_group_count


if __name__ == "__main__":
    total_population = 100000
    infection_rate = 0.0045
    false_negative_rate = 0.002
    false_positive_rate = 0.0023
    recessive_rate = 0.003
    check_counts = 0
    next_population = total_population
    next_infection_rate = infection_rate
    while True:
        if next_population > 10000:
            limit_check_size = 10000
        else:
            limit_check_size = next_population
        next_population, next_infection_rate, temp_check_counts, positive_group_count = check_disease(
            next_population, next_infection_rate, limit_check_size, false_negative_rate, false_positive_rate, recessive_rate
        )
        print(temp_check_counts)
        check_counts += temp_check_counts
        if next_population <= 2:
            break
