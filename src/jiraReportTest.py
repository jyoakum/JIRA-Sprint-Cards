#!/usr/bin/env python
# coding=utf-8
#
# author: Jerry Yoakum

"""Unit test for jiraReport.py"""

import jiraReport
import unittest

class HandleJiraContent(unittest.TestCase):
    def testRemoveHyperlink(self):
        """removeFirstLink should remove a hyperlink from a JIRA description"""
        description = "As a partner, I need response times similar to [Google|http://www.google.com]."
        description = jiraReport.removeFirstLink(description)
        self.assertIsNotNone(description)
        self.assertFalse(description.__contains__('['), msg="The description should have been stripped of it's link.")
        expectedDescription = "As a partner, I need response times similar to Google."
        self.assertEqual(description, expectedDescription, msg="The description is NOT as expected.")

if __name__ == "__main__":
    unittest.main()