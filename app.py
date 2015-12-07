# -*- coding: utf-8 -*-
"""A Flask app to visualize the infection algorithm."""

from flask import Flask, request, abort, jsonify, render_template
from werkzeug.exceptions import BadRequest
from infection import User, total_infection, limited_infection


app = Flask(__name__)


def load_user_graph():
    """Get the JSON-encoded user graph from the request body."""
    try:
        json_users = request.get_json()['users']
    except (TypeError, KeyError):
        raise BadRequest('You need to supply a JSON user graph.')
    try:
        assert isinstance(json_users, list)
        users = dict((i, User(i)) for i in range(len(json_users)))
        for i, adjacent in enumerate(json_users):
            assert isinstance(adjacent, list)
            for adjacent_id in adjacent:
                users[i].connect(users[adjacent_id])
    except KeyError as e:
        raise BadRequest('Unknown connection in graph: {0}.'.format(e.args[0]))
    except (TypeError, AssertionError):
        raise BadRequest('Users must be a list of lists.')
    return users


@app.route('/')
def home():
    """Return the home page."""
    return render_template('index.html')


@app.route('/infect', methods=['POST'])
def infect():
    """Run the specified infection algorithm on a given user graph."""
    users = load_user_graph()
    if request.args.get('type') == 'total':
        try:
            user = users[int(request.args['user'])]
        except KeyError:
            raise BadRequest('Expected a valid user in param user.')
        except ValueError:
            raise BadRequest('User must be an integer.')
        infected = total_infection(user)
        return jsonify({'users': [user.id for user in infected]})
    elif request.args.get('type') == 'limited':
        try:
            target = int(request.args['target'])
        except (KeyError, ValueError):
            raise BadRequest('Expected an integer target.')
        try:
            error = float(request.args['error']) / 100
        except (KeyError, ValueError):
            raise BadRequest('Expected an float error.')
        if error < 0 or error > 1:
            raise BadRequest('Error must be between 0 and 100.')
        groups = limited_infection(users.values(), target, error)
        if groups is None:
            users = None
        else:
            users = [u.id for group in groups for u in group]
        return jsonify({'users': users})
    raise BadRequest('Expected total or limited from query param type.')
