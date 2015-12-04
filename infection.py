# -*- coding: utf-8 -*-
"""The code."""


class User(object):

    """The user model."""

    def __init__(self, id):
        """Create a new user with the given id."""
        self.id = id
        self.adjacent = set()
        self.new_version = False

    def connect(self, other):
        """Add a new relationship."""
        self.adjacent.add(other)
        other.adjacent.add(self)


def total_infection(user):
    """Infect all the users connected to user.

    This is implemented with a depth-first search.
    """
    if user.new_version:
        return
    user.new_version = True
    for adjacent in user.adjacent:
        total_infection(adjacent)


def main():
    """The main function."""


if __name__ == '__main__':
    main()
