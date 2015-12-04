# -*- coding: utf-8 -*-
"""Test cases for infection.py, run using pytest."""

from infection import User, total_infection


def test_user_model():
    """Test the user constructor."""
    user1 = User(1)
    assert user1.id == 1
    assert not user1.new_version


def test_user_connect():
    """Test the graph connection behavior."""
    user1 = User(1)
    user2 = User(2)
    user1.connect(user2)
    assert user2 in user1.adjacent
    assert user1 in user2.adjacent


def test_total_infection():
    """This will test with a circular graph (0->1->2->0...)."""
    users = [User(i) for i in range(4)]
    users[0].connect(users[1])
    users[1].connect(users[2])
    users[2].connect(users[0])
    assert list(total_infection(users[0])) == users[:3]
