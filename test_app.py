# -*- coding: utf-8 -*-
"""Test the Flask app."""

from app import app
import json
import pytest


@pytest.fixture
def infect():
    """Return a function that calls the infect endpoint on app."""
    def inner(users, qs):
        app.debug = True
        with app.test_client() as client:
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(users)
            rv = client.post('/infect?{0}'.format(qs),
                             data=data, headers=headers)
            return json.loads(rv.data.decode())
    return inner


def post_json(client, json_text, qs=None):
    headers = {'Content-Type': 'application/json'}
    url = '/infect'
    if qs is not None:
        url += '?' + qs
    return client.post(url, headers=headers, data=json_text)


def test_bad_data():
    with app.test_client() as client:

        rv = client.post('/infect')
        assert b'You need to supply a JSON user graph.' in rv.data

        rv = post_json(client, '*&;1')
        assert b'The browser (or proxy) sent a request' in rv.data

        rv = post_json(client, '{"a": ["b"]}')
        assert b'Unknown connection in graph: b' in rv.data

        for data in ('1', '["a"]', '[0]', '{"a": 1}'):
            rv = post_json(client, data)
            assert b'Users must be a dictionary of lists' in rv.data

        rv = post_json(client, '{}')
        assert b'Expected total or limited from query param type' in rv.data

        rv = post_json(client, '{}', 'type=fake')
        assert b'Expected total or limited from query param type' in rv.data


def test_total_infection_invalid():
    with app.test_client() as client:
        headers = {'Content-Type': 'application/json'}

        rv = post_json(client, '{}', 'type=total')
        assert b'Expected a valid user in param user.' in rv.data

        rv = post_json(client, '{}', 'type=total&user=a')
        assert b'Expected a valid user in param user.' in rv.data


def test_total_infection(infect):
    users = {
        'a': ['b', 'c'],
        'b': ['d'],
        'c': ['d'],
        'd': [],
        'e': ['f', 'g', 'h'],
        'f': [],
        'g': ['h'],
        'h': ['i'],
        'i': [],
    }
    assert set(infect(users, 'type=total&user=e')['users']) == \
        set(['e', 'f', 'g', 'h', 'i'])
