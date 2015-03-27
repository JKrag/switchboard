import poc_simpletest

from helpers import *


def test_filter_continuations():
    """
    Test filter_continuations() function
    :return: None
    """
    test = poc_simpletest.TestSuite()
    # Test case empty world
    world = []
    poss_continuations = {(0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6)}
    expect = poss_continuations
    test.run_test(filter_continuations(world, poss_continuations), expect,
                  message="filter_continuations(" + str(world) + ", " + str(poss_continuations) + ")")

    # Test case: Remove one element
    world = [(0, 1, {})]
    poss_continuations = ({(0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6)})
    expect = {(0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 6)}
    test.run_test(filter_continuations(world, poss_continuations), expect,
                  message="filter_continuations(" + str(world) + ", " + str(poss_continuations) + ")")

    # Test case: surrounded
    world = [(0, 0, {}), (1, 0, {}), (2, 0, {}),
             (0, 1, {}), (2, 1, {}),
             (0, 2, {}), (1, 2, {}), (2, 2, {})]
    poss_continuations = ({(1, 1, 2), (1, 1, 3), (1, 1, 4), (1, 1, 5), (1, 1, 6)})
    expect = set()
    test.run_test(filter_continuations(world, poss_continuations), expect,
                  message="filter_continuations(" + str(world) + ", " + str(poss_continuations) + ")")

    test.report_results()


def test_continuations():
    """
    Test all_continuations() function
    :return: None
    """
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
        test.run_test(all_continuations(*args), expect, message="all_continuations(" + str(args) + ")")

    test.report_results()


def test_continuation_exits():
    """
    Test the continuation_exits() function
    :return: None
    """
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
    """
    Test the next_cell() function
    :return: None
    """
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
    """
    Test the opposite_point(p_out) function
    :return: None
    """
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
    """
    Test the track weighting function w(p_in, p_out)
    :return: None
    """
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
    test_filter_continuations()


if __name__ == "__main__":
    test_all()
