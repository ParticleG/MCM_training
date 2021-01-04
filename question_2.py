import pandas as pd

from decimal import Decimal as Dec
from calculate_group_size import calculate_group_size

header_list = ["Total population",
               "Next population",
               "Next infection rate",
               "Negative expectation",
               "Positive groups",
               "Accumulated positive groups",
               "Check counts"]
output_list = []


def check_disease(_total_population,
                  _infection_rate,
                  _previous_group_size,
                  _positive_group_cumulated,
                  _false_negative_rate,
                  _false_positive_rate,
                  _recessive_rate):
    _next_population, _negative_expect = calculate_group_size(
        _total_population,
        _infection_rate,
        0,
        _previous_group_size
    )

    _negative_rate = _negative_expect / _next_population

    _temp_false_negative_rate = \
        (Dec(1) - _negative_rate) / _negative_rate * _false_negative_rate

    _positive_group_count = _total_population / _next_population * (
            (Dec(1) - _negative_rate) +
            _false_positive_rate *
            (Dec(1) - _temp_false_negative_rate) *
            (Dec(1) - _recessive_rate) +
            (Dec(1) - _temp_false_negative_rate) * (
                    (Dec(1) - _temp_false_negative_rate) *
                    _recessive_rate + _temp_false_negative_rate
            )
    )

    _next_infection_rate = Dec(_infection_rate) / (
            Dec(1) -
            (
                    Dec(1) - _false_positive_rate -
                    _temp_false_negative_rate - _recessive_rate
            ) * (
                    _negative_expect / _next_population
            )
    )

    _check_counts = (
                            _total_population / _next_population *
                            (Dec(1) + _negative_expect / _next_population)
                    ) * _positive_group_cumulated

    _positive_group_cumulated *= _positive_group_count
    output_list.append({"Total population": round(_total_population),
                        "Next population": round(_next_population),
                        "Next infection rate": _next_infection_rate,
                        "Negative expectation": _negative_expect,
                        "Positive groups": round(_positive_group_count),
                        "Accumulated positive groups": round(
                            _positive_group_cumulated),
                        "Check counts": round(_check_counts)})
    return (_next_population, _next_infection_rate, _check_counts,
            _positive_group_count, _positive_group_cumulated)


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
    positive_group_cumulated = Dec(1)
    first_time = True
    file_name = f'Q2_{total_population}_' \
                f'{infection_rate}_' \
                f'{false_negative_rate}_' \
                f'{false_positive_rate}_' \
                f'{recessive_rate}.csv'
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
        (next_population, next_infection_rate, temp_check_counts,
         positive_group_count, positive_group_cumulated) = check_disease(
            next_population, next_infection_rate, limit_check_size,
            positive_group_cumulated, false_negative_rate, false_positive_rate,
            recessive_rate
        )
        check_counts += temp_check_counts
        first_time = False
        if last_time is True and next_population < 1:
            print(f"check_counts:{int(check_counts) + 1}")
            break
    data_frame = pd.DataFrame(output_list, columns=header_list)
    data_frame.to_csv(file_name, index=True)
