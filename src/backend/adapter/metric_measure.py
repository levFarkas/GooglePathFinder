import logging
from functools import wraps
from time import perf_counter


def metric_measure(f):

    @wraps(f)
    def inner(*args, **kwargs):
        logging.info(f"----------------------------------------------")
        logging.info(f"Execute: {f.__name__}")

        start_time = perf_counter()
        alg_result = f(*args, **kwargs)
        end_time = perf_counter()

        execution_time = end_time - start_time
        num_nodes = len(alg_result["path"])
        route_length = alg_result["distance"]
        expanded_nodes = alg_result["expanded"]

        logging.info(f"Expanded nodes: {expanded_nodes}")
        logging.info(f"Execution time: {execution_time}")
        if num_nodes:
            logging.info(f"Route computed successfully.")
            logging.info(f"Number of nodes: {num_nodes}")
            logging.info(f"Route length: {route_length}")
        else:
            logging.info(f"No solution found.")
        
        return {
            "alg_result": alg_result,
            "elapsed_time": execution_time
        }

    return inner

