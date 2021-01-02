import numpy as np


def calculate_group_size(_total_count, _infect_rate, previous_group_size):
    temp_previous_size = previous_group_size
    temp_group_size = temp_previous_size
    recent_expect = 0
    now_expect = 0
    while temp_group_size > 0:
        temp_expect = 1
        for index in np.arange(temp_group_size):
            temp_expect *= ((1 - _infect_rate) * _total_count - index) / (_total_count - index)

        old_expect = recent_expect
        recent_expect = now_expect
        now_expect = temp_expect * temp_group_size
        if old_expect < recent_expect and now_expect < recent_expect:
            positive_expect = (1 - recent_expect / temp_previous_size) * temp_previous_size
            next_count = positive_expect * (_total_count / temp_previous_size)
            print(f'When temp_total_count={_total_count}, '
                  f'temp_infect_rate={_infect_rate}, '
                  f'group_size={temp_previous_size}: '
                  f'negative_expect={recent_expect}, '
                  f'positive_expect={positive_expect}, '
                  f'next_count={next_count}')
            return temp_previous_size, recent_expect
        temp_previous_size = temp_group_size
        if temp_group_size < 100:
            temp_group_size -= 1
        else:
            temp_group_size -= int(np.round(np.log(_total_count) / np.log(6)))
