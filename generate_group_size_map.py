import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
from calculate_group_size import calculate_group_size

if __name__ == "__main__":
    total_count = 100
    limit_count = 10000
    group_size_list = []
    total_count_index = 1

    infect_rate_list = ['temp_total_count']
    infect_rate = 0.0001
    while infect_rate < 0.5:
        infect_rate_list.append(infect_rate)
        infect_rate *= 1.2

    total_count_list = []
    total_count = 100
    while total_count < 10000001:
        total_count_list.append(total_count)
        total_count *= 2

    for temp_total_count in total_count_list:
        temp_infect_rate_object = {'temp_total_count': temp_total_count}
        for temp_infect_rate in infect_rate_list[1:]:
            if temp_total_count > 10000:
                temp_check_limit = 10000
            else:
                temp_check_limit = temp_total_count
            temp_infect_rate_object[temp_infect_rate] = calculate_group_size(temp_total_count, temp_infect_rate, 0, temp_check_limit)[0]
            print(f'When temp_total_count={temp_total_count}, '
                  f'temp_infect_rate={temp_infect_rate}, '
                  f'group_size={temp_infect_rate_object[temp_infect_rate]}')
        group_size_list.append(temp_infect_rate_object)
    data_frame = pd.DataFrame(group_size_list, columns=infect_rate_list)
    data_frame.to_csv('group_size.csv', index=False)

    figure = plt.figure()
    ax = Axes3D(figure)
    x_axis, y_axis = np.meshgrid(np.log(infect_rate_list[1:]), np.log(total_count_list))
    group_size_array = list(group_size_list[0].values())[1:]
    for infect_rate_object in group_size_list[1:]:
        group_size_array = np.vstack((group_size_array, list(infect_rate_object.values())[1:]))
    ax.set_xlabel("Infection Rate [ln(rate)]")
    ax.set_ylabel("Count of population [ln(count)]")
    ax.set_zlabel("Each Group's Size")
    ax.plot_surface(x_axis, y_axis, group_size_array, cmap='rainbow', label='Group Size responded to rate and count')
    plt.show()
