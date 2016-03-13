#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import unittest
import core
import os
import config


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

