# -*- coding: utf-8 -*-
"""The code."""


class User(object):

    """The user model."""

    def __init__(self, id, version=None):
        """Create a new user with the given id."""
        self.id = id
        self.adjacent = set()
        self._version = version
        self.infection = None

    def connect(self, other):
        """Add a new relationship."""
        self.adjacent.add(other)
        other.adjacent.add(self)

    @property
    def version(self):
        """Try to get the version from the infection.

        If we aren't part of an infection, just return _version.
        """
        if self.infection is not None and self.infection.version is not None:
                return self.infection.version
        return self._version


class Infection(set):

    """A group of connected users, all running the same version."""

    def __init__(self, version=None):
        """If specified, version will be used by all contained users."""
        set.__init__(self)
        self.version = version


def infect(user, infection=None):
    """Add all users connected to user to a common infection group.

    Return the infection, or None the user already has one.

    This is just a DFS, should run in O(n) time.
    """
    if user.infection is not None:
        return None

    # Default to a new infection
    if infection is None:
        infection = Infection()

    infection.add(user)
    user.infection = infection
    for adjacent in user.adjacent:
        infect(adjacent, infection)

    return infection


def subset_sum_approx(values, key_fn, target, error):
    """Find a subset of values for which the sum is close to target.

    key_fn is a function returning the value to be summed

    A valid sum will be within error of target:

        target * (1 - error) <= sum <= target / (1 - error)
    """
    sums = [([], 0)]
    for val in values:
        added_sums = [(s + [val], t + key_fn(val)) for s, t in sums]
        sums.extend(added_sums)
        new_sums = iter(sorted(sums, key=lambda x: x[1]))
        sums = [next(new_sums)]
        for s, t in new_sums:
            if sums[-1][1] <= (1 - error) * t <= target:
                sums.append((s, t))
    if len(sums) > 0:
        # Return only numbers within our error range
        valid = list(filter(lambda s: s[1] >= (1 - error) * target, sums[-2:]))
        if len(valid) > 0:
            return min(valid, key=lambda s: abs(s[1] - target))
    return None


def total_infection(user, new_version=None):
    """Infect all the users connected to user.

    This runs in O(n).
    """
    infection = infect(user)
    infection.version = new_version
    return infection


def limited_infection(users, target, error, new_version):
    """Infect about target users with new_version.

    Find all the unique infection groups, get a subset that sums near
    the target, and infect this subset.

    Return the total number of users that were infected.
    """
    infections = list(filter(None, (infect(user) for user in users)))
    subset_sum = subset_sum_approx(infections, len, target, error)

    if subset_sum is None:
        return None

    to_infect, total = subset_sum
    for infection in to_infect:
        infection.version = new_version
    return total
