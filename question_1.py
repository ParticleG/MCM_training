from decimal import Decimal as Dec

from calculate_group_size import calculate_group_size


def check_disease(_total_population, _infection_rate, _previous_group_size, _positive_group_cumulated,
                  _false_negative_rate, _false_positive_rate, _recessive_rate):  # b,a,beta,first
    _next_population, _negative_expect = calculate_group_size(_total_population, _infection_rate, 0, _previous_group_size)
    _temp_false_negative_rate = (_next_population - _negative_expect) / _negative_expect * _false_negative_rate
    _positive_group_count = (
            Dec(_total_population) / Dec(_next_population) * ((Dec(1) - _negative_expect / _next_population) +  # Original positive groups
                                                              # False positives in negatives
                                                              _false_positive_rate * (Dec(1) - _temp_false_negative_rate) * (Dec(1) - _recessive_rate) +
                                                              # Positive groups in second check
                                                              (Dec(1) - _temp_false_negative_rate) * (
                                                                      (Dec(1) - _temp_false_negative_rate) * _recessive_rate + _temp_false_negative_rate))
    )
    _next_infection_rate = Dec(_infection_rate) / (Dec(1) - (Dec(1) - _false_positive_rate - _temp_false_negative_rate - _recessive_rate) * (
            _negative_expect / Dec(_next_population)))
    _check_counts = (_total_population / _next_population * (Dec(1) + _negative_expect / _next_population)) * _positive_group_cumulated
    _positive_group_cumulated *= _positive_group_count
    print(f"_total_population={_total_population}, "
          f"_next_population={_next_population}, "
          f"_negative_expect={_negative_expect}, "
          f"_positive_group_count={_positive_group_count}, "
          f"_positive_group_cumulated={_positive_group_cumulated}, "
          f"_next_infection_rate={_next_infection_rate}, "
          f"_check_counts={_check_counts}, ")
    return _next_population, _next_infection_rate, _check_counts, _positive_group_count, _positive_group_cumulated


if __name__ == "__main__":
    total_population = Dec(10000000)
    infection_rate = Dec('0.0045')
    false_negative_rate = Dec('0.002')
    false_positive_rate = Dec('0.002')
    recessive_rate = Dec('0.003')
    check_counts = Dec(0)
    next_population = total_population
    next_infection_rate = infection_rate
    positive_group_cumulated = Dec(1)
    first_time = True
    while True:
        last_time = False
        if next_population < 1:
            last_time = True
        if next_population > 10000:
            limit_check_size = 10000
        else:
            limit_check_size = next_population
        if first_time is True:
            first_time = False
        else:
            recessive_rate = Dec(0)
        next_population, next_infection_rate, temp_check_counts, positive_group_count, positive_group_cumulated = check_disease(
            next_population, next_infection_rate, limit_check_size, positive_group_cumulated, false_negative_rate, false_positive_rate, recessive_rate
        )
        check_counts += temp_check_counts
        first_time = False
        if last_time is True and next_population < 1:
            print(f"check_counts:{int(check_counts) + 1}")
            break
