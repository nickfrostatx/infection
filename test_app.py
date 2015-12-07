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


app.debug = True


def post_json(client, users_text, qs=None):
    headers = {'Content-Type': 'application/json'}
    url = '/infect'
    if qs is not None:
        url += '?' + qs
    data = '{"users":' + users_text + '}'
    return client.post(url, headers=headers, data=data)


def test_bad_data():
    with app.test_client() as client:

        rv = client.post('/infect')
        assert b'You need to supply a JSON user graph.' in rv.data

        rv = post_json(client, '*&;1')
        assert b'The browser (or proxy) sent a request' in rv.data

        rv = post_json(client, '[[1]]')
        assert b'Unknown connection in graph: 1' in rv.data

        for data in ('1', '"abc"', '{"1":2}', '{"0": [2]}', '{"01": []}'):
            rv = post_json(client, data)
            assert b'Users must be a list of lists' in rv.data, data

        rv = post_json(client, '[]')
        assert b'Expected total or limited from query param type' in rv.data

        rv = post_json(client, '[]', 'type=fake')
        assert b'Expected total or limited from query param type' in rv.data


def test_total_infection_invalid():
    with app.test_client() as client:
        headers = {'Content-Type': 'application/json'}

        rv = post_json(client, '[]', 'type=total')
        assert b'Expected a valid user in param user.' in rv.data

        rv = post_json(client, '[]', 'type=total&user=1')
        assert b'Expected a valid user in param user.' in rv.data

        rv = post_json(client, '[]', 'type=total&user=a')
        assert b'User must be an integer.' in rv.data


def test_total_infection(infect):
    users = {'users': [
        [1, 2],
        [3],
        [3],
        [],
        [5, 6, 7],
        [],
        [7],
        [8],
        [],
    ]}
    assert set(infect(users, 'type=total&user=4')['users']) == \
        set([4, 5, 6, 7, 8])


def test_home_page():
    with app.test_client() as client:
        rv = client.get('/')
        assert b'<title>Khan Academy Infection Demo</title>' in rv.data
        assert rv.status_code == 200
