from enum import Enum, unique
from step_2.calculate_path import calculate_path
from step_2.data_structures import FailureLearningStepResult, SuccessLearningStepResult

def execute_learning_step(dynamics, initial_state, learning_rate):
    rate_matrix = dynamics.rate_matrix.copy()
    path_with_jump_times = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path_with_jump_times is None:
        return FailureLearningStepResult()
    path = path_with_jump_times['state'].tolist()
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    pattern_state_indices = _indices_state_is_a_pattern_state(path, pattern_states)
    path_type = _determine_path_type(path, pattern_state_indices)
    match path_type:
        case PathType.EVER_LEFT_PATTERN_STATE:
            _decrease_rate_from_pattern_states(path, pattern_state_indices, rate_matrix, learning_rate)
        case PathType.NEVER_VISITED_PATTERN_STATE:
            _increase_rate_from_non_pattern_states(path, pattern_states, rate_matrix, learning_rate)
    return SuccessLearningStepResult(rate_matrix, path)

def _decrease_rate_from_pattern_states(path, pattern_state_indices, rate_matrix, learning_rate):
    index_last_state = len(path) - 1
    for pattern_state_index in pattern_state_indices:
        if pattern_state_index != index_last_state:
            pattern_state = path[pattern_state_index]
            next_state = path[pattern_state_index + 1]
            rate_matrix[pattern_state, next_state] += (learning_rate - 1) * rate_matrix[pattern_state, next_state]
            rate_matrix[next_state, pattern_state] += (learning_rate - 1) * rate_matrix[next_state, pattern_state]

def _increase_rate_from_non_pattern_states(path, pattern_states, rate_matrix, learning_rate):
    index_last_state = len(path) - 1
    for index, state in enumerate(path):
        if index != index_last_state and state not in pattern_states:
            next_state = path[index + 1]
            rate_matrix[state, next_state] += (1 / learning_rate - 1) * rate_matrix[state, next_state]
            rate_matrix[next_state, state] += (1 / learning_rate - 1) * rate_matrix[next_state, state]

def _determine_path_type(path, pattern_state_indices):
    number_of_times_visiting_pattern_state = len(pattern_state_indices)
    path_type = PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_THERE
    if number_of_times_visiting_pattern_state > 1:
        path_type = PathType.EVER_LEFT_PATTERN_STATE
    elif number_of_times_visiting_pattern_state == 1:
        if pattern_state_indices[0] != len(path) - 1:
            path_type = PathType.EVER_LEFT_PATTERN_STATE
    else:
        path_type = PathType.NEVER_VISITED_PATTERN_STATE
    return path_type

def _indices_state_is_a_pattern_state(path, pattern_states):
    indices = []
    for index, state in enumerate(path):
        if state in pattern_states:
            indices.append(index)
    return indices

@unique
class PathType(Enum):
    ARRIVED_IN_PATTERN_STATE_AND_STAYED_THERE = 1
    EVER_LEFT_PATTERN_STATE = 2
    NEVER_VISITED_PATTERN_STATE = 3