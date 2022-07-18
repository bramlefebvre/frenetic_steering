import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt

def _filter_result(result):
    return result.number_of_patterns == 2

def plot_N_calc():
    results = step_1_training_analysis_data_dao.get_training_data('data/step_1/calculation_duration_0')
    filtered_results = list(filter(_filter_result, results))

    sorted_results = {}
    for result in filtered_results:
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