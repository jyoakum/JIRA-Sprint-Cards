#!/usr/bin/env python
# coding=utf-8
#
# author: Jerry Yoakum

import base64
import easygui
import json
import os
import urllib2


def removeFirstLink(description):
    startBracket = description.find('[')
    endBracket = description.find(']') + 1
    link = description[startBracket:endBracket]

    pipe = link.find('|')
    return description.replace(link, link[1:pipe])

def getIssue(auth_header, uri):
    req = urllib2.Request(uri, headers=auth_header)
    return json.load(urllib2.urlopen(req))

def summarizeIssue(issue):
    issueSummary = '<div style="page-break-inside:avoid;max-height:400px;overflow:hidden">'
    issueSummary += '<h1>' + issue['key'] + ' - ' + issue['fields']['summary'] + '</h1>'
    description = issue['fields']['description']
    if description is None:
        description = ''
    description = description.replace('\n', '<br>')

    for i in range(description.count('[')):
        description = removeFirstLink(description)
    description = description.replace(u'—', '-')
    description = description.replace(u'’', "'")
    description = description.replace(u'‘', "'")
    description = description.replace(u'“', '"')
    description = description.replace(u'"', '"')

    storyPoints = issue['fields']['customfield_10022']
    if storyPoints is not None:
        storyPoints = float(storyPoints)
    issueSummary += '<p style="width: 550px;"><b>SP:</b> ' + str(storyPoints)\
                    + ' <b>Description</b>: ' + description + '</p>'
    for i in range(20):
        issueSummary += ('<br>')
    issueSummary += '</div><hr>'
    return issueSummary


def inputbox(message, title, default=None, private=False):
    if private:
        response = easygui.passwordbox(msg=message, title=title, default=default)
    else:
        response = easygui.enterbox(msg=message, title=title, default=default)
    if response is None:
        exit(0)
    else:
        return response


def main():
    jiraHostname = inputbox("Please enter the hostname for your JIRA service. "
                            "It will be used like so: https://{hostname}/rest/api/latest/issue/{issue}",
                            title="JIRA Hostname", default="jira.ean")
    username = inputbox("Please enter your JIRA username.", title="Username")
    password = inputbox("Please enter your JIRA password.", title="Password", private=True)
    issues = inputbox("Please enter the JIRA issues in a comma delimited format.",
                      title="JIRA Issues", default='APIDEV-714, APIDEV-728, KC-167')

    issues = issues.upper().split(',')
    auth_header = { 'Authorization' : 'Basic ' + base64.b64encode(username + ':' + password) }
    out = open("./jira_report.html", 'w')
    out.write('<html><body>')

    for issue in issues:
        uri = 'https://' + jiraHostname + '/rest/api/latest/issue/' + issue.strip()
        out.write(summarizeIssue(getIssue(auth_header, uri)))

    out.write('</body></html>')
    out.close()
    os.system("open ./jira_report.html")


if __name__ == '__main__':
    main()