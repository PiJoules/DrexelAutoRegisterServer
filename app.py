#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json

from flask import Flask, request, jsonify
from uuid import uuid64

# Create flask obj
app = Flask(__name__)
app.secret_key = str(uuid64())


def response(code, message=""):
    """Wrapper for response message."""
    return jsonify(
        code=code,
        message=message
    ), code


def add_user(user_id, crns):
    """Add the user and courses to the database."""
    # TODO: add logic for adding user to db
    pass


###############
# ROUTES
##############

@app.route("/")
def index_route():
    return "Nothing to see here"


@app.route("/add_user", methods=["POST"])
def add_user_route():
    """Route for adding a user ID and the crns to the database."""
    # Get params
    user_id = request.args.get("id", None)
    crns = request.args.get("crns", None)

    # Check params
    if user_id is None:
        return response(400, "'id' was not provided.")
    if crns is None:
        return response(400, "'crns' was not provided.")
    try:
        user_id = int(user_id)
    except ValueError:
        return response(400, "'id' must be an integer.")
    try:
        crns = json.loads(crns)
    except ValueError:
        return response(400, "'crns' must be valid json.")

    add_user(user_id, crns)
    return response(200, "Successfully added user.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)

