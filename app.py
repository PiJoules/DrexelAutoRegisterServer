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


def register_user(user_id, email, encrypted_psswd, crns):
    """Register a user for classes using twil."""
    # TODO: find out what to call from twil component
    pass


def validate_drexel_email(email):
    """Make sure the email provided is a valid drexel email."""
    import re
    email_pattern = re.compile("\w{2,3}\d{2,3}\@drexel\.edu")
    return email_pattern.match(email)


def get_crns(user_id):
    """Get the crns for this user from the db."""
    return []


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
    user_id = request.form.get("id", None)
    crns = request.form.get("crns", None)

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

    # Add user
    add_user(user_id, crns)

    # Return response
    return response(200, "Successfully added user.")


@app.route("/register_user")
def register_user_route():
    """Route for registering a user for classes when timeticket passes."""
    # Get params
    user_id = request.form.get("id", None)
    email = request.form.get("email", None)
    encrypted_psswd = request.form.get("password", None)

    # Check params
    try:
        user_id = int(user_id)
    except ValueError:
        return response(400, "'id' must be an integer.")
    if not validate_drexel_email(email):
        return response(400, "'{}' is an invalid drexel email.".format(email))

    # Get the crns for this user
    crns = get_crns(user_id)

    # Register users
    register_user(user_id, email, encrypted_psswd, crns)

    # Return response
    return response(200, "Successfully registered for classes.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)

