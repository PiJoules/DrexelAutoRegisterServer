#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import unittest
import app
import core
import os
import config

from mock import patch


class TestApp(unittest.TestCase):
    """Class for testing the app."""

    @patch("app.add_user")
    @patch("app.response")
    @patch("app.request")
    def test_add_user_route(self, req_mock, resp_mock, au_mock):
        """Test that the add_user_route works properly."""
        # Test no id
        req_mock.form = {}
        app.add_user_route()
        resp_mock.assert_called_with(400, "'id' was not provided.")

        # Test no email
        req_mock.form = {"id": 1}
        app.add_user_route()
        resp_mock.assert_called_with(400, "'email' was not provided.")

        # Test no crns
        req_mock.form = {"id": 1, "email": "abc123@drexel.edu"}
        app.add_user_route()
        resp_mock.assert_called_with(400, "'crns' was not provided.")

        # Test invalid email
        req_mock.form = {
            "id": 1,
            "email": "invalid email",
            "crns": '["12345"]'
        }
        app.add_user_route()
        resp_mock.assert_called_with(
            400, "Invalid email provided.")

        # Works properly
        req_mock.form = {
            "id": 1,
            "email": "abc123@drexel.edu",
            "crns": '["12345"]'
        }
        app.add_user_route()
        au_mock.assert_called_with(1, "abc123@drexel.edu", ["12345"])
        resp_mock.assert_called_with(200, "Successfully added user.")

    @patch("app.register_user")
    @patch("app.response")
    @patch("app.request")
    def test_register_user_route(self, req_mock, resp_mock, ru_mock):
        """Test that the add_user_route works properly."""
        # Test no id
        req_mock.form = {}
        app.register_user_route()
        resp_mock.assert_called_with(400, "'id' was not provided.")

        # Test no email
        req_mock.form = {"id": 1}
        app.register_user_route()
        resp_mock.assert_called_with(400, "'email' was not provided.")

        # Test no password
        req_mock.form = {"id": 1, "email": "abc123@drexel.edu"}
        app.register_user_route()
        resp_mock.assert_called_with(400, "'password' was not provided.")

        # Test invalid email
        req_mock.form = {
            "id": 1,
            "email": "invalid email",
            "password": 'something'
        }
        app.register_user_route()
        resp_mock.assert_called_with(
            400, "Invalid email provided.")

        # Test no crns for this id
        req_mock.form = {
            "id": "9999999999999999999",  # Hopefully this dir doesn't exists
            "email": "abc123@drexel.edu",
            "password": 'something'
        }
        app.register_user_route()
        resp_mock.assert_called_with(
            400, "The user with id '9999999999999999999' does not exist.")

        # Test bad user_id/email combo
        req_mock.form = {
            "id": "1",
            "email": "abc123@drexel.edu",
            "password": 'something'
        }
        with patch("app.get_crns") as gc_mock:
            gc_mock.return_value = None
            app.register_user_route()
            resp_mock.assert_called_with(
                400, "The user_id '1' is not associated with the email "
                "'abc123@drexel.edu'.")

        # Success
        with patch("app.get_crns") as gc_mock:
            gc_mock.return_value = "crns"
            app.register_user_route()
            ru_mock.assert_called_with("abc123@drexel.edu", "something",
                                       "crns")
            resp_mock.assert_called_with(
                200, "Successfully registered for classes.")


class TestCore(unittest.TestCase):
    """Test core fuctions."""

    def test_validate_user_crns(self):
        """Test that a list of crns as a json string is valid."""
        # Test invalid crns (not json)
        result = core.validate_crns_str("invalid")
        self.assertEqual(result, (False, "'crns' must be valid json."))

        # Test invalid crns (not a list)
        result = core.validate_crns_str('{"12345": 45678}')
        self.assertEqual(result,
                         (False, "The crns must be an array of strings."))

        # Test invalid crns (not a list of strins)
        result = core.validate_crns_str('[12345]')
        self.assertEqual(result,
                         (False, "The crns must be an array of strings."))

        # Test invalid crns (not length 5)
        result = core.validate_crns_str('["0123"]')
        self.assertEqual(result,
                         (False, "The crns must be an array of strings."))

    def test_user_functions(self):
        """Test that a user is successfully added."""
        # Add user.
        core.add_user("some user id", "abc123@drexel.edu", ["12345"])

        # Get crns
        crns = core.get_crns("some user id", "abc123@drexel.edu")
        self.assertEqual(crns, ["12345"])

        # Delete afterwards
        os.remove(os.path.join(config.USERS_DIR, "some user id"))


if __name__ == "__main__":
    unittest.main()

