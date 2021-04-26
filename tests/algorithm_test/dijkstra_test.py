from GooglePathFinder.src.algorithm.dijkstra import Dijkstra
from GooglePathFinder.src.model.node import Node


def test_dijkstra_predefined_match():
    """
    Compare the output to a manually computed solution
    The graph features the following corner cases:
    - update required of an already queued node
    - intermediate node without neighbors (no outgoing edge)
    """

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
    s.set_neighbors([[3, d], [9, e], [1, i]])
    a.set_neighbors([])
    b.set_neighbors([[2, a]])
    c.set_neighbors([[2, a]])
    d.set_neighbors([[1, b], [8, c], [2, e]])
    e.set_neighbors([[9, k], [1, h], [14, f]])
    f.set_neighbors([[5, g]])
    h.set_neighbors([[4, j], [4, i]])
    i.set_neighbors([[15, j]])
    j.set_neighbors([[3, k]])
    k.set_neighbors([[5, f]])
    g.set_neighbors([])

    solver = Dijkstra()
    manual_solution = (["d", "e", "h", "j", "k", "f", "g"], 23)
    (path, sum_distance) = solver.run(s, g)

    assert (path, sum_distance) == manual_solution


def test_dijkstra_emptyqueue_unmatched():
    # Nodes
    s = Node("s")  # Start node
    g = Node("g")  # End node

    # Neighbors
    s.set_neighbors([])
    g.set_neighbors([])

    solver = Dijkstra()
    manual_solution = ([], float("inf"))
    (path, sum_distance) = solver.run(s, g)

    assert (path, sum_distance) == manual_solution


def test_dijkstra_multigraph_match():
    """
    The graph contains loops (edges defined by the same vertex)
    """

    # Nodes
    s = Node("s")  # Start node
    a = Node("a")
    b = Node("b")
    g = Node("g")  # End node

    # Neighbors
    s.set_neighbors([[3, a]])
    a.set_neighbors([[1, a], [3, b]])
    b.set_neighbors([[1, b], [2, a], [3, g]])
    g.set_neighbors([])

    solver = Dijkstra()
    manual_solution = (["a", "b", "g"], 9)
    (path, sum_distance) = solver.run(s, g)

    assert (path, sum_distance) == manual_solution


def test_dijkstra_direct_path_match():
    """
    Direct path between the start and end node
    """

    # Nodes
    s = Node("s")  # Start node
    g = Node("g")  # End node

    # Neighbors
    s.set_neighbors([[1, g]])
    g.set_neighbors([])

    solver = Dijkstra()
    manual_solution = (["g"], 1)
    (path, sum_distance) = solver.run(s, g)

    assert (path, sum_distance) == manual_solution
