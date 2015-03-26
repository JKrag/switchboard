import poc_simpletest
# This is being prototyped in CodeSkulptor: http://www.codeskulptor.org/#user39_rWIkR8a2nk_5.py
# The testing framework will only work there, but could easily be modified for other framework locally.

# Prototyping logical switchboard auto-routing
# The switchboard is represented by a grid of cells, with x, y coords
# starting from upper left corner (to make mapping to canvas easier)

# Each cell has 8 possible entry/exit points, and they are numbered
# clockwise from upper left, starting with zero:
#
# 012  012  012
# 7 3  7 3  7 3
# 654  654  654
# \  |  /
# 012  012  012
# 7 3--7 3--7 3
#                   654  654  654
#                      /  | \
#                   012  012  012
#                   7 3  7 3  7 3
#                   654  654  654
#
# We support 3 types of tracks, in all rotations:
#     1. Straight tracks, horz., vert, or diag. e.g. 0-4, 1-5, 7-3
#     2. Soft curve, e.g. 1-4, 1-6
#     3. 90 deg. hard curve, e.g. 1-3, 1-7
#


def w(a, b):
    """Calculate the 'weight' of a track piece going from
    entry point a to exit point b in a cell.
    possible results are:
        0 = A straight track - very good
        1 = A soft curve - ok
        2 = A hard curve - not so good
        3 = A fold-back - not acceptable
    """
    # Basically we find the circle distance between a and b (diff % 8)
    # This gives 4 for straight, 3 or 5 for soft, 2 or 6 for hard curve
    c = (a - b) % 8
    # Then we shift down 4 to be symmetric around zero, and get absolute value
    # This makes the two directions of curves give same result.
    return abs(c - 4)


def opposite_point(n):
    return (n + 4) % 8


def next_cell(x, y, exit):
    """
    Given a cell, and its exit point, return the coordinates
    of the next cell and entry point.
    """
    new_x = x
    new_y = y
    if exit in (0, 1, 2):
        new_y -= 1
    if exit in (4, 5, 6):
        new_y += 1
    if exit in (2, 3, 4):
        new_x += 1
    if exit in (0, 7, 6):
        new_x -= 1
    entry = opposite_point(exit)
    return new_x, new_y, entry


def continuation_exits(entry):
    """
    Given a cell and an entry point, find all the possible exit points.
    """
    all_corners = {0, 1, 2, 3, 4, 5, 6, 7}
    return all_corners - {entry, (entry + 1) % 8, (entry - 1) % 8}


def continuations(x, y, entry):
    """
    Given a cell and an entry point, find all the possible exit points.
    """
    exit_corners = continuation_exits(entry)
    return {(x, y, c) for c in exit_corners}


def test_continuations():
    known_results = [((0, 0, 0), {(0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6)}),
                     ((0, 0, 1), {(0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6), (0, 0, 7)}),
                     ((0, 0, 2), {(0, 0, 4), (0, 0, 5), (0, 0, 6), (0, 0, 7), (0, 0, 0)}),
                     ((0, 0, 3), {(0, 0, 5), (0, 0, 6), (0, 0, 7), (0, 0, 0), (0, 0, 1)}),
                     ((0, 0, 4), {(0, 0, 6), (0, 0, 7), (0, 0, 0), (0, 0, 1), (0, 0, 2)}),
                     ((0, 0, 5), {(0, 0, 7), (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)}),
                     ((0, 0, 6), {(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4)}),
                     ((0, 0, 7), {(0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5)})]

    test = poc_simpletest.TestSuite()
    for args, expect in known_results:
        test.run_test(continuations(*args), expect, message="continuations(" + str(args) + ")")

    test.report_results()


def test_continuation_exits():
    known_results = [(0, {2, 3, 4, 5, 6}),
                     (1, {3, 4, 5, 6, 7}),
                     (2, {4, 5, 6, 7, 0}),
                     (3, {5, 6, 7, 0, 1}),
                     (4, {6, 7, 0, 1, 2}),
                     (5, {7, 0, 1, 2, 3}),
                     (6, {0, 1, 2, 3, 4}),
                     (7, {1, 2, 3, 4, 5})]

    test = poc_simpletest.TestSuite()
    for arg, expect in known_results:
        test.run_test(continuation_exits(arg), expect, message="continuation_exits(" + str(arg) + ")")

    test.report_results()


def test_next_cell():
    # args and expected result are in the format x, y, direction,
    # where (x, y) are the coordinates of the cell, and direction
    # is the exit point from this cell
    known_results = [((4, 8, 3), (5, 8, 7)),
                     ((4, 8, 4), (5, 9, 0)),
                     ((4, 8, 5), (4, 9, 1)),
                     ((1, 1, 7), (0, 1, 3)),
                     ((4, 8, 0), (3, 7, 4))]

    test = poc_simpletest.TestSuite()
    for args, expect in known_results:
        test.run_test(next_cell(*args), expect, message="next_cell(" + str(args) + ")")

    test.report_results()


def test_opposite_point():
    known_results = [(0, 4),
                     (1, 5),
                     (2, 6),
                     (3, 7),
                     (4, 0),
                     (5, 1),
                     (6, 2),
                     (7, 3)]

    test = poc_simpletest.TestSuite()
    for val, expect in known_results:
        test.run_test(opposite_point(val), expect, message="opposite_point(" + str(val) + ")")

    test.report_results()


def test_w():
    test = poc_simpletest.TestSuite()
    test.run_test(w(0, 4), 0, message="w(0,4)")
    test.run_test(w(1, 5), 0, message="w(1,5)")
    test.run_test(w(2, 6), 0, message="w(2,6)")
    test.run_test(w(3, 7), 0, message="w(3,7)")
    test.run_test(w(4, 8), 0, message="w(4,8)")
    test.run_test(w(5, 1), 0, message="w(5,1)")
    test.run_test(w(6, 2), 0, message="w(6,2)")
    test.run_test(w(7, 3), 0, message="w(7,3)")

    test.run_test(w(0, 3), 1, message="w(0,3)")
    test.run_test(w(0, 5), 1, message="w(0,5)")
    test.run_test(w(1, 4), 1, message="w(1,4)")
    test.run_test(w(1, 6), 1, message="w(1,6)")
    test.run_test(w(2, 5), 1, message="w(2,5)")
    test.run_test(w(2, 7), 1, message="w(2,7)")
    test.run_test(w(3, 0), 1, message="w(3,0)")
    test.run_test(w(3, 6), 1, message="w(3,6)")
    test.run_test(w(4, 1), 1, message="w(4,1)")
    test.run_test(w(4, 7), 1, message="w(4,7)")
    test.run_test(w(5, 0), 1, message="w(5,0)")
    test.run_test(w(5, 2), 1, message="w(5,2)")
    test.run_test(w(6, 1), 1, message="w(6,1)")
    test.run_test(w(6, 3), 1, message="w(6,3)")
    test.run_test(w(7, 2), 1, message="w(7,2)")
    test.run_test(w(7, 4), 1, message="w(7,4)")

    test.run_test(w(7, 5), 2, message="w(7,5)")
    test.run_test(w(5, 7), 2, message="w(5,7)")
    test.run_test(w(7, 1), 2, message="w(7,1)")
    test.run_test(w(1, 7), 2, message="w(1,7)")
    test.run_test(w(0, 2), 2, message="w(0,2)")

    test.run_test(w(1, 2), 3, message="w(1,2)")
    test.run_test(w(0, 1), 3, message="w(0,1)")
    test.run_test(w(7, 0), 3, message="w(7,0)")
    test.report_results()


def test_all():
    test_w()
    test_opposite_point()
    test_next_cell()
    test_continuations()
    test_continuation_exits()


test_all()
