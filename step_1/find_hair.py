from dataclasses import dataclass
from typing import Iterable
import numpy
import numpy.typing as npt
from typing import TypeVar

from step_1.data_structures import BasinUnderConstruction
from step_1.find_disentangled_system import HairFindingProgressForBasin

random_number_generator = numpy.random.default_rng()

def find_hair(graph, hair_finding_progress_for_basin, basins: tuple[BasinUnderConstruction, ...]):
    free_vertices = _get_free_vertices(len(graph), basins)
    if len(free_vertices) == 0:
        find_hair_response = FindHairResponse(None, None, False, True)
    else:
        hair_length = hair_finding_progress_for_basin.length_of_hair_to_find
        path = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
        if path is None:
            hair_length += 1
            path = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
            if path is None:
                find_hair_response = FindHairResponse(None, None)
            else:
                find_hair_response = FindHairResponse(path[0], path[1], True)
        else:
            find_hair_response = FindHairResponse(path[0], path[1])
    return find_hair_response


    
@dataclass(frozen = True)
class FindHairResponse:
    new_vertex: int | None
    destination_vertex: int | None
    increase_length_of_hair_to_find: bool = False
    no_free_vertices_anymore: bool = False


def _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length):
    if hair_length == 1:
        path = _find_hair_of_length_1(graph, hair_finding_progress_for_basin, free_vertices)
    else:
        path = _find_hair_of_length_longer_than_1(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
    return path

def _find_hair_of_length_1(graph, hair_finding_progress_for_basin, free_vertices):
    possibilities = [(first_vertex, end_vertex) for first_vertex in free_vertices for end_vertex in hair_finding_progress_for_basin.non_pattern_vertices_in_a_cycle if graph[first_vertex, end_vertex] == 1]
    if len(possibilities) == 0:
        return None
    else:
        return _pick_one_arc(possibilities)

def _find_hair_of_length_longer_than_1(graph, hair_finding_progress_for_basin, free_vertices, hair_length):
    shuffled_free_vertices = list(free_vertices)
    random_number_generator.shuffle(shuffled_free_vertices)
    for new_vertex in shuffled_free_vertices:
        hair_vertex = _get_fitting_hair_vertex(new_vertex, graph, hair_finding_progress_for_basin, hair_length)
        if hair_vertex is not None:
            return (new_vertex, hair_vertex)
    


# def _get_fitting_hair_vertex(path, graph, hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices):
#     already_present_hair_vertex = _check_already_present_hair_vertices(path, graph, hair_finding_progress_for_basin)
#     if already_present_hair_vertex is None:
#         return None
        # if hair_finding_progress_for_basin.length_of_hair_to_find - len(path) == 1:
        #     _finish_path_with_available_vertex(path, graph, hair_finding_progress_for_basin, free_vertices)
        # else:
        #     pass
        # available_vertices = _get_forward_available_vertices(path, graph, free_vertices)

    # else:
    #     new_path = path.copy()
    #     new_path.append(already_present_hair_vertex)
    #     return new_path


# def _check_already_present_hair_vertices(path, graph, hair_finding_progress_for_basin):
#     already_present_hair_vertices = _get_forward_already_present_hair_vertices(path, graph, hair_finding_progress_for_basin)
#     for already_present_hair_vertex in already_present_hair_vertices:
#         if _length_already_present_hair_fits(hair_finding_progress_for_basin, already_present_hair_vertex):
#             return already_present_hair_vertex



def _get_fitting_hair_vertex(new_vertex, graph, hair_finding_progress_for_basin: HairFindingProgressForBasin, hair_length):
    hair_vertices = [vertex for vertex in hair_finding_progress_for_basin.hair_vertices if graph[new_vertex, vertex] == 1 and _length_already_present_hair_fits(hair_finding_progress_for_basin, hair_length, vertex)]
    if len(hair_vertices) == 0:
        return None
    else:
        return _pick_one(hair_vertices)
    
def _length_already_present_hair_fits(hair_finding_progress_for_basin: HairFindingProgressForBasin, hair_length, already_present_hair_vertex):
    number_of_vertices_left_to_add = hair_length - 1
    number_of_vertices_on_hair_starting_from_already_present_hair_vertex = _number_of_vertices_on_hair_starting_from_already_present_hair_vertex(hair_finding_progress_for_basin, already_present_hair_vertex)
    return number_of_vertices_left_to_add == number_of_vertices_on_hair_starting_from_already_present_hair_vertex

def _number_of_vertices_on_hair_starting_from_already_present_hair_vertex(hair_finding_progress_for_basin: HairFindingProgressForBasin, already_present_hair_vertex):
    number = 1
    arcs = hair_finding_progress_for_basin.basin.arcs
    destination = _destination_arc_starting_from_vertex(arcs, already_present_hair_vertex)
    while destination in hair_finding_progress_for_basin.hair_vertices:
        number += 1
        destination = _destination_arc_starting_from_vertex(arcs, destination)
    return number
        

def _destination_arc_starting_from_vertex(arcs, vertex):
    destinations_of_arcs_starting_from_vertex = [arc[1] for arc in arcs if arc[0] == vertex]
    assert len(destinations_of_arcs_starting_from_vertex) == 1
    return destinations_of_arcs_starting_from_vertex[0]

def _get_free_vertices(number_of_vertices: int, basins: tuple[BasinUnderConstruction, ...]):
    vertices_in_a_basin = set()
    vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - vertices_in_a_basin

def _get_forward_available_vertices(path, graph, free_vertices):
    last_vertex_of_path = path[-1]
    available_vertices = [vertex for vertex in set(free_vertices) - set(path) if graph[last_vertex_of_path, vertex] == 1]
    random_number_generator.shuffle(available_vertices)
    return available_vertices

def _pick_one_arc(arcs: Iterable[tuple[int, int]]) -> tuple[int, int]:
    return random_number_generator.choice(list(arcs))

def _pick_one(vertices: Iterable[int]) -> int:
    return random_number_generator.choice(list(vertices))
