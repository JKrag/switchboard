# This was originally started in CodeSkulptor: http://www.codeskulptor.org/#user39_rWIkR8a2nk_5.py

# Prototyping logical switchboard auto-routing
# The switchboard is represented by a grid of cells, with x, y coords
# starting from upper left corner (to make mapping to canvas easier)

# Each cell has 8 possible entry/exit points, and they are numbered
# clockwise from upper left, starting with zero:
# @formatter:off
#
#                   012  012  012
#                   7 3  7 3  7 3
#                   654  654  654
#                      \  |  /
#                   012  012  012
#                   7 3--7 3--7 3
#                   654  654  654
#                      /  | \
#                   012  012  012
#                   7 3  7 3  7 3
#                   654  654  654
#
# @formatter:on
#
# We support 3 types of tracks, in all rotations:
# 1. Straight tracks, horz., vert, or diag. e.g. 0-4, 1-5, 7-3
# 2. Soft curve, e.g. 1-4, 1-6
# 3. 90 deg. hard curve, e.g. 1-3, 1-7
#


def w(a, b):
    """
    Calculate the 'weight' of a track piece going from
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


def opposite_point(p_out):
    """
    Given an exit point in one cell, return the number of the matching
    entry point in the "next" cell.
    :param p_out: the number of the exit point (0..7)
    :return: the number of the matching entry point in the next cell
    """
    return (p_out + 4) % 8


def next_cell(x, y, p_out):
    """
    Given a cell, and its exit point, return the coordinates
    of the next cell and entry point.
    :param x: The x coord. of the current cell
    :param y: The y coord. of the current cell
    :param p_out: The exit point from the current cell
    :return: A tuple (x, y, p_in) with the coordinates and entry point for the next cell.
    """
    new_x = x
    new_y = y
    if p_out in (0, 1, 2):
        new_y -= 1
    if p_out in (4, 5, 6):
        new_y += 1
    if p_out in (2, 3, 4):
        new_x += 1
    if p_out in (0, 7, 6):
        new_x -= 1
    entry = opposite_point(p_out)
    return new_x, new_y, entry


def continuation_exits(p_in):
    """
    Given an entry point to a cell, return all the possible exit points.
    There should always be 5 possible exits, based on
    a straight track, slight curve right and left, and sharp curve right and left.
    :param p_in: The entry point to a cell
    :return: A set of 5 exit points
    """
    all_corners = {0, 1, 2, 3, 4, 5, 6, 7}
    cw = (p_in + 1) % 8  # clockwise point
    ccw = (p_in - 1) % 8  # counter clockwise point
    return all_corners - {p_in, cw, ccw}


def all_continuations(x, y, p_in):
    """
    Given a cell and an entry point, find all the possible exit points.
    :param x: X-coord of current cell
    :param y: Y-coord of current cell
    :param p_in: entry point on current cell
    :return: set of (x, y, p_out) where x, y are always the provided cell, and p_out are the possible exit points.
    """
    exit_corners = continuation_exits(p_in)
    return {(x, y, c) for c in exit_corners}


def filter_continuations(current_world, continuations):
    """
    Remove those continuations that are not legal given the provided world state
    :param current_world: A sequence of cell coordinates (x, y, {...}) of cells that are currently in use
    :param continuations: A set of (x, y, p_out), where (x, y) are cell coordinates, and p_out is a numbered exit point
    :return: The given input continuations, filtering out those that are illegal in the provided world
    """

    # Currently we are only concerned with whether a cell is occupied, e.g. is it in the world set.
    # Therefore we only need the x, y from the tuples
    c_world = map(lambda cw: cw[:2], current_world)
    no_good = lambda c: next_cell(*c)[:2] not in c_world

    return set(filter(lambda c: no_good(c), continuations))

