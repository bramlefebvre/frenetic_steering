from daos.step_2_training_results_dao import save_training_results
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from step_2.data_structures import TrainingResult
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
import util

def generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns):
    minimal_initial_activity_parameter = 1 / 10 * number_of_states / number_of_patterns
    return [minimal_initial_activity_parameter * x for x in range(1, 21)]

def generate_training_set_size_list(number_of_states):
    return [number_of_states * x for x in range(1, 6)]

def generate_exuberant_systems(number_of_states, number_of_patterns):
    patterns = util.generate_single_state_patterns(number_of_states, number_of_patterns)
    exuberant_systems = []
    for i in range(10):
        tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
        for j in range(10):
            exuberant_system = find_exuberant_system(tournament_and_patterns)
            id = {
                'number_of_states': number_of_states,
                'number_of_patterns': number_of_patterns,
                'tournament_and_patterns_index': i,
                'exuberant_system_index': j
            }
            exuberant_system.id = id
            exuberant_systems.append(exuberant_system)
    return exuberant_systems

number_of_states_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/calculation_duration_0'

def train():
    for number_of_states in number_of_states_list:
        training_results = []
        number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            exuberant_systems = generate_exuberant_systems(number_of_states, number_of_patterns)
            initial_activity_parameter_factors = generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns)
            for initial_activity_parameter_factor in initial_activity_parameter_factors:
                training_set_size_list = generate_training_set_size_list(number_of_states)
                for training_set_size in training_set_size_list:
                    print('[number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size]:')
                    print([number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size])
                    for exuberant_system in exuberant_systems:
                        initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
                        trained_dynamics = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                        
                        # training_result = TrainingResult(success, exuberant_system.id, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance)
                        # training_results.append(training_result)
        save_training_results(training_results, filename)