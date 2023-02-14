'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.Moon_version.find_disentangled_system import find_disentangled_system
import analysis_util
import cProfile
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.data_structures import LearningAlgorithm

number_of_states = 100
number_of_patterns = 10

patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)

exuberant_system = find_disentangled_system(tournament_and_patterns, True).disentangled_system
print('exuberant system found')
initial_dynamics = initialize_dynamics(exuberant_system, 5, 5, 1)
cProfile.run('train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 400)', 'data/step_2_profiler_data_2')