#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module handling routing for server.
"""

from __future__ import print_function

import json

from flask import Flask, request
from uuid import uuid4
from core import response, validate_drexel_email, add_user, register_user
from core import get_crns, create_working_dir

# Create flask obj
app = Flask(__name__)
app.secret_key = str(uuid4())


###############
# ROUTES
##############


@app.route("/add_user", methods=["POST"])
def add_user_route():
    """
    Route for adding a user ID and the crns to the database.

    params
    id:
        Unique ID associated with the user. This is generated on the client
        and is not meant to be viewed by the user (or anyone else). It should
        also not be in plain text. Having a unique ID unknown to users will
        allow us to add a layer of security such that users will not be able
        to register classes for other users.
    email:
        The user's drexel email.
    crns:
        JSON string that is just an array of crns as ints.
    """
    # Get params
    user_id = request.form.get("id", None)
    email = request.form.get("email", None)
    crns = request.form.get("crns", None)

    # Check params
    if user_id is None:
        return response(400, "'id' was not provided.")
    if crns is None:
        return response(400, "'crns' was not provided.")

    # Check types
    try:
        user_id = int(user_id)
    except ValueError:
        return response(400, "'id' must be an integer.")
    try:
        crns = json.loads(crns)
    except ValueError:
        return response(400, "'crns' must be valid json.")
    if not email or not validate_drexel_email(email):
        return response(400, "Invalid email provided.")

    # Add user
    add_user(user_id, email, crns)

    # Return response
    return response(200, "Successfully added user.")


@app.route("/register_user", methods=["POST"])
def register_user_route():
    """
    Route for registering a user for classes when timeticket passes.

    params:
    id:
        The unique ID associated with the user. This is the same as the one
        passed earlier in the add_user_route.
    email:
        User email. This must be the same email associeated with the ID sent
        in add_user_route and this message.
    password:
        Encrypted password. This is done on the user end, but the server must
        also know the encryption algorithm to decrypt it.
    """
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
    try:
        crns = get_crns(user_id)
    except IOError:
        return response(400,
                        "The user with id '{}' does not exist."
                        .format(user_id))
    if crns is None:
        return response(400,
                        ("The user_id '{}' is not associated with the "
                         "email '{}'".format(user_id, email)))

    # Register users
    register_user(email, encrypted_psswd, crns)

    # Return response
    return response(200, "Successfully registered for classes.")


if __name__ == "__main__":
    create_working_dir()
    app.run(debug=True, port=8080)

