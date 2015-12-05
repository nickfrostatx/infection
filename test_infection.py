# -*- coding: utf-8 -*-
"""Test cases for infection.py, run using pytest."""

from infection import User, Infection, infect, total_infection, \
    limited_infection
import pytest


@pytest.fixture
def circular_users():
    num_users = 3
    users = [User(i, 1) for i in range(num_users)]
    for i in range(num_users):
        users[i].connect(users[(i + 1) % num_users])
    return users


def test_user_model():
    """Test the user constructor."""
    user1 = User(1, 1)
    assert user1.id == 1
    assert user1.version == 1


def test_user_connect():
    """Test the graph connection behavior."""
    user1 = User(1)
    user2 = User(2)
    user1.connect(user2)
    assert user2 in user1.adjacent
    assert user1 in user2.adjacent


def test_infection_model():
    """Make sure users pull version from their infection."""
    user = User(1, 1)
    assert user.version == 1
    infection = Infection(2)
    user.infection = infection
    infection.add(user)
    assert user.version == 2


def test_infect(circular_users):
    """Check our infect model on a circular graph"""
    infection = infect(circular_users[0])
    for user in circular_users:
        assert user in infection
        assert user.infection == infection


def test_total_infection(circular_users):
    """This will test with a circular graph (0->1->2->0...)."""
    total_infection(circular_users[0], 2)
    for user in circular_users:
        assert user.version == 2


def test_limited_infection(monkeypatch):
    """Test that limited_infection properly uses subset sum output."""
    users = [User(i, 1) for i in range(5)]
    users[0].connect(users[1])
    users[1].connect(users[2])
    users[3].connect(users[4])
    # Override subset_sum_approx to just return the 0, 1, 2 group
    monkeypatch.setattr('infection.subset_sum_approx',
                        lambda *a: ([users[0].infection], 0))
    limited_infection(users, 3, 2)
    for user in users[:3]:
        assert user.version == 2
    for user in users[3:]:
        assert user.version == 1
