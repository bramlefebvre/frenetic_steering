import numpy
from step_2.data_structures import FailureTrainingResult, LearningAlgorithm, SuccessTrainingResult, TrainingResultStatus
import daos.base_dao as base_dao

def save_training_results(training_results, filename):
    serialized_training_results = list(map(_serialize_training_result, training_results))
    base_dao.add_data_no_duplicates(serialized_training_results, filename)

def get_training_results(filename):
    serialized_training_results = base_dao.read_data(filename)
    return list(map(_deserialize_training_result, serialized_training_results))

def _deserialize_training_result(serialized):
    status = TrainingResultStatus(serialized['status'])
    if status == TrainingResultStatus.SUCCESS:
        return _deserialize_success_training_result(serialized)
    else:
        return _deserialize_failure_training_result(serialized)

def _deserialize_success_training_result(serialized):
    exuberant_system_id = serialized['exuberant_system_id']
    driving_value = serialized['driving_value']
    travel_time = serialized['travel_time']
    learning_rate = serialized['learning_rate']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    training_set_size = serialized['training_set_size']
    performance = serialized['performance']
    rate_matrix = numpy.array(serialized['rate_matrix'])
    id = serialized['id']
    return SuccessTrainingResult(exuberant_system_id, driving_value, travel_time, learning_rate, algorithm, training_set_size, performance, rate_matrix, id)

def _deserialize_failure_training_result(serialized):
    exuberant_system_id = serialized['exuberant_system_id']
    driving_value = serialized['driving_value']
    travel_time = serialized['travel_time']
    learning_rate = serialized['learning_rate']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    step_number = serialized['step_number']
    id = serialized['id']
    return FailureTrainingResult(exuberant_system_id, driving_value, travel_time, learning_rate, algorithm, step_number, id)

def _serialize_training_result(training_result):
    if training_result.status == TrainingResultStatus.SUCCESS:
        return _serialize_success_training_result(training_result)
    else:
        return _serialize_failure_training_result(training_result)

def _serialize_success_training_result(training_result):
    serialized = _serialize_base_training_result(training_result)
    serialized['training_set_size'] = training_result.training_set_size
    serialized['performance'] = training_result.performance
    serialized['rate_matrix'] = training_result.rate_matrix.tolist()
    return serialized

def _serialize_failure_training_result(training_result):
    serialized = _serialize_base_training_result(training_result)
    serialized['step_number'] = training_result.step_number
    return serialized

def _serialize_base_training_result(training_result):
    serialized = {
        'exuberant_system_id': training_result.exuberant_system_id,
        'status': training_result.status.value,
        'driving_value': training_result.driving_value,
        'travel_time': training_result.travel_time,
        'learning_rate': training_result.learning_rate,
        'algorithm': training_result.algorithm.id
    }
    if training_result.id is not None:
        serialized['id'] = training_result.id
    return serialized