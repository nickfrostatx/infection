# -*- coding: utf-8 -*-
"""A Flask app to visualize the infection algorithm."""

from flask import Flask, request, abort, jsonify
from werkzeug.exceptions import BadRequest
from infection import User, total_infection, limited_infection


app = Flask(__name__)


def load_user_graph():
    """Get the JSON-encoded user graph from the request body."""
    json_users = request.get_json()
    if json_users is None:
        raise BadRequest('You need to supply a JSON user graph.')
    try:
        users = dict((str(id), User(str(id))) for id in json_users)
        for id in json_users:
            for adjacent_id in json_users[id]:
                users[str(id)].connect(users[str(adjacent_id)])
    except KeyError as e:
        raise BadRequest('Unknown connection in graph: {0}.'.format(e.args[0]))
    except TypeError:
        raise BadRequest('Users must be a dictionary of lists.')
    return users


@app.route('/infect', methods=['POST'])
def infect():
    """Run the specified infection algorithm on a given user graph."""
    users = load_user_graph()
    if request.args.get('type') == 'total':
        try:
            user = users[request.args['user']]
        except KeyError:
            raise BadRequest('Expected a valid user in param user.')
        infected = total_infection(user)
        return jsonify({'users': [user.id for user in infected]})
    elif request.args.get('type') == 'limited':
        return jsonify({'users': []})
    raise BadRequest('Expected total or limited from query param type.')
