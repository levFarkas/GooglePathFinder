from GooglePathFinder.src.algorithm.bi_astar import BiAStar
from GooglePathFinder.src.algorithm.heuristics import node_l2distance
from GooglePathFinder.src.model.node import Node
from GooglePathFinder.src.backend.services.mocks.mock_distance_service import MockDistanceService


def test_biastar_predefined_match():
    """
    Compare the output to a manually computed solution
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s")  # Start node
    a = Node("a", 12, 35)
    b = Node("b", 8, 15)
    c = Node("c", 5, 12)
    d = Node("d", 3, 4)
    e = Node("e", 3, 4)
    f = Node("f", 9, 40)
    h = Node("h", 15, 8)
    i = Node("i", 12, 5)
    j = Node("j", 7, 24)
    k = Node("k", 39, 80)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[3, d], [9, e], [1, i]])
    mock_service.set_neighbors(a, [])
    mock_service.set_neighbors(b, [[2, a]])
    mock_service.set_neighbors(c, [[2, a]])
    mock_service.set_neighbors(d, [[1, b], [8, c], [2, e]])
    mock_service.set_neighbors(e, [[9, k], [1, h], [14, f]])
    mock_service.set_neighbors(f, [[5, g]])
    mock_service.set_neighbors(h, [[4, j], [4, i]])
    mock_service.set_neighbors(i, [[15, j]])
    mock_service.set_neighbors(j, [[3, k]])
    mock_service.set_neighbors(k, [[5, f]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["d", "e", "f", "g"], 24)
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_biastar_emptyqueue_unmatched():
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s", 1, 1)  # Start node
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [])
    mock_service.set_neighbors(g, [])

    manual_solution = ([], float("inf"))
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_biastar_multigraph_match():
    """
    The graph contains loops (edges defined by the same vertex)
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[3, a]])
    mock_service.set_neighbors(a, [[1, a], [3, b]])
    mock_service.set_neighbors(b, [[1, b], [2, a], [3, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["a", "b", "g"], 9)
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_biastar_direct_path_match():
    """
    Direct path between the start and end node
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s", 10, 10)  # Start node
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[1, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["g"], 1)
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_biastar_odd_length_match():
    """
    The path has an odd length
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[3, a]])
    mock_service.set_neighbors(a, [[3, b]])
    mock_service.set_neighbors(b, [[3, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["a", "b", "g"], 9)
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_biastar_even_length_match():
    """
    The path has an even length
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    c = Node("c", 1, 1)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[3, a]])
    mock_service.set_neighbors(a, [[3, b]])
    mock_service.set_neighbors(b, [[3, c]])
    mock_service.set_neighbors(c, [[1, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["a", "b", "c", "g"], 10)
    result = BiAStar.run(s, g, node_l2distance, mock_service)

    assert (result['path'], result['distance']) == manual_solution
