from daos.step_2_training_analysis_data_dao import save_training_data
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from analysis_step_2.data_structures import TrainingAnalysisData
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance
import analysis_util

number_of_states_list = [100]
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_AVOID_CYCLES
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/training_data_1'

def generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns):
    fraction = 1 / 10 * number_of_states / number_of_patterns
    return [fraction * 4]

def generate_training_set_size_list(number_of_states):
    return [number_of_states * 4]

def train():
    for number_of_states in number_of_states_list:
        training_results = []
        # number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        number_of_patterns_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        for number_of_patterns in number_of_patterns_list:
            exuberant_systems = analysis_util.generate_exuberant_systems(number_of_states, number_of_patterns)
            initial_activity_parameter_factors = generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns)
            for initial_activity_parameter_factor in initial_activity_parameter_factors:
                training_set_size_list = generate_training_set_size_list(number_of_states)
                for training_set_size in training_set_size_list:
                    print('[number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size]:')
                    print([number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size])
                    for exuberant_system in exuberant_systems:
                        initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
                        training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                        if training_result.success:
                            performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
                        else: 
                            performance = None
                        training_result = TrainingAnalysisData(exuberant_system.id, training_result.success, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
                        training_results.append(training_result)
        save_training_data(training_results, filename)