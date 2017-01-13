#!/usr/bin/env python

import imaplib
import email
import os
import sys
import csv


def connectToServer(username, password):
    '''Authenticate user and connect to email server'''
    try:
        server = imaplib.IMAP4_SSL('imap.gmail.com')  # hard coded to gmail
        server.login(username, password)
    except imaplib.IMAP4.error as e:
        print("Unable to log in: {}".format(e))
        sys.exit()
    return server


def parseMessageBody(content):
    '''Parse the body message from the email contents'''
    body = ""
    for uid, email in content.items():
        # Message body extraction adopted from Todor
        # http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
        # Begin adopted content
        if email.is_multipart():
            for part in email.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                # Skip attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email.get_payload(decode=True)
        # End adopted content
    body.rstrip()
    return body


def saveContentToFile(content, body):
    ''' Write email content to CSV '''
    with open('part1_results.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        # Write the csv header line
        writer.writerow(('UID', 'Subject', 'Sender', 'Recipient', 'Date', 'Message_body'))
        for uid, email in content.items():
            writer.writerow((uid, email['subject'], email['from'], email['to'], email['date'], body))


def retrieveMail(server, subject):
    '''Retrieve email from the given server and list of search terms'''
    # Use Gmail's all mail folder to retrieve from everywhere
    server.select("[Gmail]/All Mail", readonly=True)
    content = dict()

    # Iterate through search terms
    for subj in subject:
        response, data = server.uid('search', None, '(SUBJECT "' + subj + '")')
        for mailID in data[0].split():
            # fetch based on uid instead of sequential id
            response, mailContent = server.uid('fetch', mailID, '(RFC822)')
            # convert from MIME format to email message using Python's email module
            content[mailID] = email.message_from_string(mailContent[0][1])

    body = parseMessageBody(content)
    saveContentToFile(content, body)


if __name__ == '__main__':
    # normally would prompt for credentials and discard them or store encrypted
    server = connectToServer('returnpath.test.kevin@gmail.com', 'test123!')

    # searchTerms = ['Home depot', '1800flowers', 'netflix']
    searchTerms = ['home depot with attachment']
    retrieveMail(server, searchTerms)

    # cleanup
    server.close()
    server.logout()
