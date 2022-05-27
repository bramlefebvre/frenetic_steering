from enum import Enum, unique
from step_2.calculate_path import calculate_path
from step_2.data_structures import Action, FailureLearningStepResult, RateChangeInstruction, SuccessLearningStepResult


def execute_learning_step(dynamics, initial_state, learning_rate):
    rate_matrix = dynamics.rate_matrix.copy()
    path_with_jump_times = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path_with_jump_times is None:
        return FailureLearningStepResult()
    path = path_with_jump_times['state'].tolist()
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    transitions = _to_transitions(path)
    path_type = _determine_path_type(transitions, pattern_states)
    graph = dynamics.exuberant_system.graph
    input = RateChangeInstructionFunctionInput(graph, path, transitions, pattern_states)
    rate_change_instructions = rate_change_instructions_function_map[path_type](input)
    _apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate)
    return SuccessLearningStepResult(rate_matrix, path)

def _ever_left_pattern_state_rate_change_instructions(input):
    transitions = input.transitions
    pattern_states = input.pattern_states
    leaving_transitions = []
    for transition in transitions:
        if _is_a_leaving_transition(transition, pattern_states):
            leaving_transitions.append(transition)
    rate_change_instructions = []
    for transition in leaving_transitions:
        rate_change_instructions.append(RateChangeInstruction(transition, Action.DECREASE))
    return rate_change_instructions

def _never_visited_pattern_state_rate_change_instructions(input):
    transitions = set(input.transitions)
    forward_transitions = _get_forward_transitions(transitions, input.graph)
    backward_transitions = transitions - forward_transitions
    forward_arcs_from_start_states_backward_transitions = _arcs_going_forward_from_start_states_backward_transitions(backward_transitions, input.graph)
    forward_arcs_from_last_state_of_path = _arcs_going_forward_from_last_state_of_path(input)
    transitions_to_rate_change = forward_transitions | forward_arcs_from_start_states_backward_transitions | forward_arcs_from_last_state_of_path
    rate_change_instructions = []
    for transition in transitions_to_rate_change:
        rate_change_instructions.append(RateChangeInstruction(transition, Action.INCREASE))
    return rate_change_instructions

def _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions(input):
    pattern_state_that_was_left = input.transitions[-1][1]
    graph_values_for_state = input.graph[pattern_state_that_was_left, :]
    rate_change_instructions = []
    for state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            rate_change_instructions.append(RateChangeInstruction((pattern_state_that_was_left, state), Action.DECREASE))
    return rate_change_instructions


def _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions(input):
    return []

def _is_a_leaving_transition(transition, pattern_states):
    return transition[0] in pattern_states



def _apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate):
    for rate_change_instruction in rate_change_instructions:
        transition = rate_change_instruction.transition
        factor = _get_factor_rate_change(rate_change_instruction.action, learning_rate)
        rate_matrix[transition[0], transition[1]] += factor * rate_matrix[transition[0], transition[1]]
        rate_matrix[transition[1], transition[0]] += factor * rate_matrix[transition[1], transition[0]]


def _get_factor_rate_change(action, learning_rate):
    if action == Action.INCREASE:
        return 1 / learning_rate - 1
    else:
        assert action == Action.DECREASE
        return learning_rate - 1

def _arcs_going_forward_from_last_state_of_path(input):
    last_state = input.transitions[-1][1]
    graph_values_for_state = input.graph[last_state, :]
    arcs = set()
    for state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            arcs.add((last_state, state))
    return arcs

def _arcs_going_forward_from_start_states_backward_transitions(backward_transitions, graph):
    start_states_backward_transitions = set()
    for backward_transition in backward_transitions:
        start_states_backward_transitions.add(backward_transition[0])
    forward_arcs = set()
    for start_state in start_states_backward_transitions:
        graph_values_from_start_state = graph[start_state, :]
        for state, graph_value in enumerate(graph_values_from_start_state):
            if graph_value == 1:
                forward_arcs.add((start_state, state))
    return forward_arcs
    
def _get_forward_transitions(transitions, graph):
    forward_transitions = set()
    for transition in transitions:
        if graph[transition[0], transition[1]] == 1:
            forward_transitions.add(transition)
    return forward_transitions








def _to_transitions(path):
    index_last_state = len(path) - 1
    transitions = []
    for index, state in enumerate(path):
        if index != index_last_state:
            transitions.append((state, path[index + 1]))
    return transitions

def _determine_path_type(transitions, pattern_states):
    path_type = PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH
    if _ever_left_pattern_state(transitions, pattern_states):
        path_type = PathType.EVER_LEFT_PATTERN_STATE
    else:
        if _arrived_in_pattern_state(transitions, pattern_states):
            pass
        else:
            path_type = PathType.NEVER_VISITED_PATTERN_STATE
    return path_type

def _arrived_in_pattern_state(transitions, pattern_states):
    arrived_in_pattern_state = transitions[-1][1] in pattern_states
    if arrived_in_pattern_state:
        assert _other_transitions_dont_contain_pattern_states(transitions, pattern_states)
    return arrived_in_pattern_state

def _other_transitions_dont_contain_pattern_states(transitions, pattern_states):
    index_last_transition = len(transitions) - 1
    for index, transition in transitions:
        if index != index_last_transition:
            if transition[0] in pattern_states or transition[1] in pattern_states:
                return False
    return transitions[-1][0] in pattern_states

def _ever_left_pattern_state(transitions, pattern_states):
    for transition in transitions:
        if transition[0] in pattern_states:
            return True
    return False

class RateChangeInstructionFunctionInput:
    def __init__(self, graph, path, transitions, pattern_states):
        self.graph = graph
        self.path = path
        self.transitions = transitions
        self.pattern_states = pattern_states

@unique
class PathType(Enum):
    ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH = 1
    EVER_LEFT_PATTERN_STATE = 2
    NEVER_VISITED_PATTERN_STATE = 3
    ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON = 4

def _initialize_rate_change_instructions_function_map():
    rate_change_instructions_function_map = {
        PathType.EVER_LEFT_PATTERN_STATE: _ever_left_pattern_state_rate_change_instructions,
        PathType.NEVER_VISITED_PATTERN_STATE: _never_visited_pattern_state_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON: _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH: _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions
    }
    return rate_change_instructions_function_map
rate_change_instructions_function_map = _initialize_rate_change_instructions_function_map()