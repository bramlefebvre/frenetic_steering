'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


import frenetic_steering.daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt

def _filter_result(result):
    return result.number_of_patterns == 2

def plot_s_calc():
    training_data_list = step_1_training_analysis_data_dao.get_training_data('data/step_1/eliminate_cycles/calc_sv_p5')
    # filtered_results = list(filter(_filter_result, results))

    sorted_results = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list = []
    calculation_duration_list = []
    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        number = 0
        summed_calculation_durations = 0
        for result in results:
            number += 1
            summed_calculation_durations += result.calculation_duration
        calculation_duration_list.append(summed_calculation_durations / number)
    plt.scatter(number_of_states_list, calculation_duration_list)
    plt.xlabel('number of states')
    plt.ylabel('calculation duration (ms)')
    plt.show()
