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


from statistics import mean
from frenetic_steering.daos.step_1_training_analysis_data_dao import save_training_data
from frenetic_steering.step_1.data_structures import TrainingAnalysisData
from frenetic_steering.step_1.find_disentangled_system import find_disentangled_system
import timeit
import time
import frenetic_steering.analysis_util as analysis_util
from frenetic_steering.daos.graphs_and_patterns_dao import generate_single_tournament_and_patterns
import frenetic_steering.daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao

def _get_mean(getter, results):
    data = [getter(result) for result in results]
    return mean(data)

def _get_mean_duration(results):
    return _get_mean(lambda x: x.calculation_duration, results)

low = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
high = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

number_of_states_list = [1000]
number_of_patterns_list = [10]

def calculation_duration():
    for number_of_states in number_of_states_list:
        results = []
        # number_of_patterns_list = analysis_util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(100):
                patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                timer = timeit.Timer(lambda: find_disentangled_system(tournament_and_patterns), timer = time.process_time)
                times_executed, total_duration = timer.autorange()
                calculation_duration =  (total_duration / times_executed) * 10 ** 3
                result = TrainingAnalysisData(number_of_states, number_of_patterns, 1, None, calculation_duration)
                results.append(result)
        save_training_data(results, 'data/step_1/calc_s1000_p10')


def print_mean_duration():
    training_data_list = step_1_training_analysis_data_dao.get_training_data('data/step_1/calc_s1000_p10')
    print(_get_mean_duration(training_data_list))
    




