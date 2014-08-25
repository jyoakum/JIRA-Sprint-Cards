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


    def descriptionTester(self, description):
        """Test helper to test Descriptions."""
        issue = {u'key': u'APIDEV-714', u'fields':
            {
                u'customfield_10022': '3',
                u'description': description,
                u'reporter':
                    {
                        u'displayName': u'Nathan England',
                        u'name': u'nengland',
                        u'self': u'https://jira.ean/rest/api/2/user?username=nengland',
                        u'emailAddress': u'nengland@expedia.com',
                        u'active': True
                    },
                u'summary': u'Gradle Plug-in: Sonar for Meta projects',
            }, u'self': u'https://jira.ean/rest/api/latest/issue/26957', u'id': u'26957'
        }
        issueSummary = jiraReport.summarizeIssue(issue)
        self.assertIsNotNone(issueSummary)
        expectedSummary = u'<div style="page-break-inside:avoid;max-height:400px;overflow:hidden">'\
                          + u'<h1>APIDEV-714 - Gradle Plug-in: Sonar for Meta projects</h1>'\
                          + u'<p style="width: 550px;"><b>SP:</b> 3.0 <b>Description</b>: </p>'\
                          + u'<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'\
                          + u'</div><hr>'
        self.assertEqual(issueSummary,
                         expectedSummary,
                         msg="The issueSummary is NOT as expected.\nissueSummary: " + issueSummary
                             + "\nexpectedSummary: " + expectedSummary)


    def testDescriptions(self):
        """Don't fail when JIRA description is empty."""
        self.descriptionTester(None)
        self.descriptionTester('')

if __name__ == "__main__":
    unittest.main()