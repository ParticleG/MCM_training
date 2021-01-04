import pandas as pd

from decimal import Decimal as Dec
from calculate_group_size import calculate_group_size

header_list = ["Total population",
               "Group size",
               "Next population",
               "Next infection rate",
               "Negative rate",
               "Check counts"]
output_list = []


def check_disease(_total_population,
                  _infection_rate,
                  _previous_group_size,
                  _false_negative_rate,
                  _false_positive_rate,
                  _recessive_rate):
    _group_size, _negative_expect = \
        calculate_group_size(_total_population,
                             _infection_rate,
                             0,
                             _previous_group_size)

    _negative_rate = _negative_expect / _group_size

    _next_population = _total_population * (
            Dec(1) -
            (
                    (
                            Dec(1) -
                            (
                                    _false_positive_rate + _recessive_rate +
                                    (Dec(1) - _negative_rate) /
                                    _negative_rate * _false_negative_rate
                            )
                    ) * _negative_rate
            )
    )

    _next_infection_rate = \
        _total_population / _next_population * _infection_rate

    _check_counts = _total_population / _group_size * (Dec(1) + _negative_rate)

    output_list.append({"Total population": round(_total_population),
                        "Group size": round(_group_size),
                        "Next population": round(_next_population),
                        "Next infection rate": _next_infection_rate,
                        "Negative rate": _negative_rate,
                        "Check counts": round(_check_counts)})
    return _next_population, _next_infection_rate, _check_counts, _group_size


if __name__ == "__main__":
    inputs = input(
        "Please enter "
        "<Total population> "
        "<Infection rate> "
        "<False negative rate> "
        "<False positive rate> "
        "<Recessive rate>").split(" ")
    if len(inputs) != 5:
        print("Invalid arguments.")
        exit(1)
    total_population = Dec(inputs[0])
    infection_rate = Dec(inputs[1])
    false_negative_rate = Dec(inputs[2])
    false_positive_rate = Dec(inputs[3])
    recessive_rate = Dec(inputs[4])
    check_counts = Dec(0)
    next_population = total_population
    next_infection_rate = infection_rate
    first_time = True
    file_name = f'Q3_{total_population}_' \
                f'{infection_rate}_' \
                f'{false_negative_rate}_' \
                f'{false_positive_rate}_' \
                f'{recessive_rate}.csv'
    while True:
        if next_population > 10000:
            limit_check_size = 10000
        else:
            limit_check_size = next_population
        if first_time is True:
            first_time = False
        else:
            recessive_rate = Dec(0)
        next_population, next_infection_rate, temp_check_counts, group_size = \
            check_disease(
                next_population, next_infection_rate, limit_check_size,
                false_negative_rate, false_positive_rate, recessive_rate
            )
        check_counts += temp_check_counts
        first_time = False
        if group_size < 1:
            print(f"check_counts:{int(check_counts) + 1}")
            break
    data_frame = pd.DataFrame(output_list, columns=header_list)
    data_frame.to_csv(file_name, index=True)
