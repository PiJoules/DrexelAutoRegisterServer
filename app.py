#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module handling routing for server.
"""

from __future__ import print_function

import json

from register import register
from flask import Flask, request
from uuid import uuid4
from core import response, create_working_dir

# Create flask obj
app = Flask(__name__)
app.secret_key = str(uuid4())


###############
# ROUTES
##############

@app.route("/register_user", methods=["POST"])
def register_user_route():
    """
    Route for registering a user for classes when timeticket passes.

    id:
        The drexel ID associated with the user.
    password:
        Drexel login password.
    crns:
        JSON string that is just an array of crns as ints.
    """
    # Get params
    user_id = request.form.get("id", None)
    psswd = request.form.get("password", None)
    crns = request.form.get("crns", None)
    print(user_id, psswd, crns)

    # Check params
    try:
        assert isinstance(user_id, basestring)
        assert isinstance(psswd, basestring)

        crns = json.loads(crns)
        assert isinstance(crns, list)
        assert all(isinstance(x, basestring) and len(x) == 5 for x in crns)
    except Exception:
        return response(
            400, "Error: Invalid types supplied. Make sure the user_id, "
            "password, and crns are all valid.")

    # Register users
    errors = register(user_id, psswd, crns)
    print("errors: ", map(str, errors))

    # Return response
    if not errors:
        return response(200, "Successfully registered for classes.")
    else:
        error_msg = "Failed to register crns: "
        error_msg += ", ".join("{} ({})".format(err.crn, err.status)
                               for err in errors)
        return response(400, error_msg)


if __name__ == "__main__":
    create_working_dir()
    app.run(debug=True, port=8080, host="0.0.0.0")

