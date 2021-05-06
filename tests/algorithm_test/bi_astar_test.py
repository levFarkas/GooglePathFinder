from src.algorithm.bi_astar import BiAStar
from src.algorithm.heuristics import node_l2distance
from src.model.node import Node


def test_biastar_predefined_match():
    """
    Compare the output to a manually computed solution
    """

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

    solver = BiAStar()
    manual_solution = (["d", "e", "f", "g"], 24)
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution


def test_biastar_emptyqueue_unmatched():
    # Nodes
    s = Node("s", 1, 1)  # Start node
    g = Node("g", 0, 0)  # End node

    # Neighbors
    s.set_neighbors([])
    g.set_neighbors([])

    solver = BiAStar()
    manual_solution = ([], float("inf"))
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution


def test_biastar_multigraph_match():
    """
    The graph contains loops (edges defined by the same vertex)
    """

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    s.set_neighbors([[3, a]])
    a.set_neighbors([[1, a], [3, b]])
    b.set_neighbors([[1, b], [2, a], [3, g]])
    g.set_neighbors([])

    solver = BiAStar()
    manual_solution = (["a", "b", "g"], 9)
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution


def test_biastar_direct_path_match():
    """
    Direct path between the start and end node
    """

    # Nodes
    s = Node("s", 10, 10)  # Start node
    g = Node("g", 0, 0)  # End node

    # Neighbors
    s.set_neighbors([[1, g]])
    g.set_neighbors([])

    solver = BiAStar()
    manual_solution = (["g"], 1)
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution


def test_biastar_odd_length_match():
    """
    The path has an odd length
    """

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    s.set_neighbors([[3, a]])
    a.set_neighbors([[3, b]])
    b.set_neighbors([[3, g]])
    g.set_neighbors([])

    solver = BiAStar()
    manual_solution = (["a", "b", "g"], 9)
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution


def test_biastar_even_length_match():
    """
    The path has an even length
    """

    # Nodes
    s = Node("s", 10, 10)  # Start node
    a = Node("a", 3, 4)
    b = Node("b", 2, 2)
    c = Node("c", 1, 1)
    g = Node("g", 0, 0)  # End node

    # Neighbors
    s.set_neighbors([[3, a]])
    a.set_neighbors([[3, b]])
    b.set_neighbors([[3, c]])
    c.set_neighbors([[1, g]])
    g.set_neighbors([])

    solver = BiAStar()
    manual_solution = (["a", "b", "c", "g"], 10)
    (path, sum_distance) = solver.run(s, g, node_l2distance)

    assert (path, sum_distance) == manual_solution
