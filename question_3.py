from decimal import Decimal as Dec

from calculate_group_size import calculate_group_size


def check_disease(_total_population, _infection_rate, _previous_group_size,
                  _false_negative_rate, _false_positive_rate, _recessive_rate):  # b,a,beta,first
    _group_size, _negative_expect = calculate_group_size(_total_population, _infection_rate, 0, _previous_group_size)
    _temp_false_negative_rate = (_group_size - _negative_expect) / _negative_expect * _false_negative_rate
    _negative_population = _total_population * (_negative_expect / _group_size)
    _negative_infection_rate = _temp_false_negative_rate + _recessive_rate

    _true_negative_group_size, _true_negative_expect = calculate_group_size(_negative_population, _negative_infection_rate, 0, _negative_population)
    _true_negative_population = _negative_population * (_true_negative_expect / _true_negative_group_size)
    _false_negative_population = _negative_population * (Dec(1) - _true_negative_expect / _true_negative_group_size)

    _positive_population = _total_population * (Dec(1) - _negative_expect / _group_size) + _false_negative_population

    _positive_infection_rate = _positive_population
    print(f"_total_population={_total_population}, "
          f"_group_size={_group_size}, "
          f"_negative_expect={_negative_expect}, "
          f"_negative_population={_negative_population}, "
          f"_positive_population={_positive_population}, "
          f"_next_infection_rate={_next_infection_rate}, "
          f"_check_counts={_check_counts}, ")
    return _group_size, _next_infection_rate, _check_counts, _positive_group_count


if __name__ == "__main__":
    total_population = Dec(10000000)
    infection_rate = Dec('0.0045')
    false_negative_rate = Dec('0.002')
    false_positive_rate = Dec('0.002')
    recessive_rate = Dec('0.003')
    check_counts = Dec(0)
    next_population = total_population
    next_infection_rate = infection_rate
    while True:
        is_last_check = False
        if next_population < 1:
            is_last_check = True
        if next_population > 10000:
            limit_check_size = 10000
        else:
            limit_check_size = next_population
        next_population, next_infection_rate, temp_check_counts, positive_group_count = check_disease(
            next_population, next_infection_rate, limit_check_size, false_negative_rate, false_positive_rate, recessive_rate
        )
        check_counts += temp_check_counts
        first_time = False
        if is_last_check is True and next_population < 1:
            print(f"check_counts:{int(check_counts) + 1}")
            break
