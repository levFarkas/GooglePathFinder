from functools import wraps
from time import perf_counter


def metric_measure(f):

    @wraps(f)
    def inner(*args, **kwargs):
        start_time = perf_counter()
        alg_result = f(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        return {
            "alg_result": alg_result,
            "elapsed_time": execution_time
        }

    return inner

