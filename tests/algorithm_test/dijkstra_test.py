from GooglePathFinder.src.algorithm.dijkstra import Dijkstra
from GooglePathFinder.src.model.node import Node
from GooglePathFinder.src.backend.services.mocks.mock_distance_service import MockDistanceService


def test_dijkstra_predefined_match():
    """
    Compare the output to a manually computed solution
    The graph features the following corner cases:
    - update required of an already queued node
    - intermediate node without neighbors (no outgoing edge)
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s")  # Start node
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    e = Node("e")
    f = Node("f")
    h = Node("h")
    i = Node("i")
    j = Node("j")
    k = Node("k")
    g = Node("g")  # End node

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

    manual_solution = (["d", "e", "h", "j", "k", "f", "g"], 23)
    result = Dijkstra.run(s, g, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_dijkstra_emptyqueue_unmatched():
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s")  # Start node
    g = Node("g")  # End node

    # Neighbors
    mock_service.set_neighbors(s, [])
    mock_service.set_neighbors(g, [])

    manual_solution = ([], float("inf"))
    result = Dijkstra.run(s, g, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_dijkstra_multigraph_match():
    """
    The graph contains loops (edges defined by the same vertex)
    """
    mock_service = MockDistanceService()

    # Nodes
    s = Node("s")  # Start node
    a = Node("a")
    b = Node("b")
    g = Node("g")  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[3, a]])
    mock_service.set_neighbors(a, [[1, a], [3, b]])
    mock_service.set_neighbors(b, [[1, b], [2, a], [3, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["a", "b", "g"], 9)
    result = Dijkstra.run(s, g, mock_service)

    assert (result['path'], result['distance']) == manual_solution


def test_dijkstra_direct_path_match():
    """
    Direct path between the start and end node
    """
    mock_service = MockDistanceService()


    # Nodes
    s = Node("s")  # Start node
    g = Node("g")  # End node

    # Neighbors
    mock_service.set_neighbors(s, [[1, g]])
    mock_service.set_neighbors(g, [])

    manual_solution = (["g"], 1)
    result = Dijkstra.run(s, g, mock_service)

    assert (result['path'], result['distance']) == manual_solution
