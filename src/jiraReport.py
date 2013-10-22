#!/usr/bin/env python
# coding=utf-8
#
# author: Jerry Yoakum

import urllib2, json, base64, easygui, os


def removeFirstLink(description):
    startBracket = description.find('[')
    endBracket = description.find(']') + 1
    link = description[startBracket:endBracket]

    pipe = link.find('|')
    return description.replace(link, link[1:pipe])


def writeIssue(auth_header, issue, fileHandler):
    uri = 'https://jira.ean/rest/api/latest/issue/' + issue

    req = urllib2.Request(uri, headers=auth_header)
    result = json.load(urllib2.urlopen(req))
    fileHandler.write('<div style="page-break-inside:avoid;max-height:400px;overflow:hidden">')
    fileHandler.write('<h1>' + result['key'] + ' - ' + result['fields']['summary'] + '</h1>')
    description = result['fields']['description']
    description = description.replace('\n', '<br>')

    for i in range(description.count('[')):
        description = removeFirstLink(description)
    description = description.replace(u'—', '-')

    storyPoints = result['fields']['customfield_10022']
    if storyPoints is not None:
        storyPoints = float(storyPoints)
    fileHandler.write('<p style="width: 550px;"><b>SP:</b> ' + str(storyPoints)
                      + ' <b>Description</b>: ' + description + '</p>')
    for i in range(20):
        fileHandler.write('<br>')
    fileHandler.write('</div><hr>')

def main():
    username = easygui.enterbox("Please enter your JIRA username.", title="Username")
    password = easygui.passwordbox("Please enter your JIRA password.", title="Password")
    issues = easygui.enterbox("Please enter the JIRA issues in a comma delimited format.",
                              title="JIRA Issues", default='APIDEV-714, APIDEV-728, KC-167')

    if username is not None and password is not None and issues is not None:
        issues = issues.upper().split(',')
        auth_header = { 'Authorization' : 'Basic ' + base64.b64encode(username + ':' + password) }
        out = open("./jira_report.html", 'w')
        out.write('<html><body>')

        for issue in issues:
            writeIssue(auth_header, issue.strip(), out)

        out.write('</body></html>')
        out.close()
        os.system("open ./jira_report.html")


if __name__ == '__main__':
    main()