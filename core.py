#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module containing core functionality of the app.

File hierarchy:
working_dir/
- classes/
  - crn1 (json - class data)
  - crn2 (json - class data)
  - crn3 (json - class data)
- users/
  - userid1 (json - crns)
  - userid2 (json - crns)
  - userid3 (json - crns)

- Have all users in separate files as opposed to 1 file to avoid problems
  with different processes reading/writing to the same file.
- Have all users/classes be userid/crn for easy access.
"""

from __future__ import print_function

import os
import json
import errno

from flask import jsonify


def create_working_dir():
    """Attempt to create the directories specified in the config."""
    import config
    dirs = (config.WORKING_DIR, config.USERS_DIR, config.CLASSES_DIR)
    for dirname in dirs:
        try:
            os.mkdir(dirname)
        except OSError as e:
            # Ignore error relating to directory already exists
            if e.errno != errno.EEXIST:
                raise RuntimeError(
                    "Could not create directory '{}'".format(dirname))


def response(code, message=""):
    """Wrapper for response message."""
    return jsonify(
        code=code,
        message=message
    ), code


def add_user(user_id, email, crns):
    """
    Add the user and courses to the filesystem.

    user_id: str
    email: str (validated)
    crns: list of ints (validated)
    """
    from config import USERS_DIR
    filename = os.path.join(USERS_DIR, user_id)
    with open(filename, "w") as user:
        user.write(json.dumps({
            "email": email,
            "crns": crns
        }))


def register_user(email, encrypted_psswd, crns):
    """Register a user for classes using twil."""
    # TODO: find out what to call from twil component
    pass


def validate_drexel_email(email):
    """Make sure the email provided is a valid drexel email."""
    import re
    email_pattern = re.compile("\w{2,3}\d{2,3}\@drexel\.edu")
    return email_pattern.match(email)


def validate_crns_str(crns_str):
    """
    Validate an array of crns as a json string.

    return:
        - (False, Error message as string is failed.)
        - (True, The crns list.)
    """
    try:
        # Must be valid json
        crns = json.loads(crns_str)
    except ValueError:
        return False, "'crns' must be valid json."
    try:
        # Must be list
        assert isinstance(crns, list)

        # Must be strings.
        # This is just in case we may have a crn that starts with 0.
        # In this case, converting to an int will trim the 0 and add
        # slightly more work for me adding the zeros back.
        assert all(isinstance(x, basestring) for x in crns)

        # Each crn must be length 5
        assert all(len(x) == 5 for x in crns)
    except AssertionError:
        return False, "The crns must be an array of strings."
    return True, crns


def get_crns(user_id, email):
    """
    Get the crns for this user from the db.

    user_id: str
    email: str (validated)

    throws: IOError if file does not exist

    return:
        - List of crns as ints if successful.
        - None if user id does not correspond with the email.
    """
    from config import USERS_DIR
    filename = os.path.join(USERS_DIR, user_id)
    with open(filename, "r") as user:
        user_data = json.load(user)
        if user_data["email"] != email:
            return None
        return user_data["crns"]

