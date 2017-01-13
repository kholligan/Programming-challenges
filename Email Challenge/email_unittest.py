import unittest
import emailsearch_part1
import email
import os
import filecmp


class EmailTests(unittest.TestCase):
    def test_csv_output(self):
        goldFilePath = 'test_email_csv.csv'
        with open('./Test_Email/test_msg_attachment.txt', 'r') as infile:
            test_message = dict()
            test_message_content = infile.read()
            test_message['1'] = email.message_from_string(test_message_content)
            emailsearch_part1.saveContentToFile(test_message, "example body")
            self.assertTrue(filecmp.cmp('part1_results.csv', goldFilePath))

    def test_message_body(self):
        with open('./Test_Email/test_msg_attachment.txt', 'r') as infile:
            expected_test_result = "See attachment\r\n"
            test_message = dict()
            test_message_content = infile.read()
            test_message['1'] = email.message_from_string(test_message_content)
            body = emailsearch_part1.parseMessageBody(test_message)
            self.assertEqual(expected_test_result, body)

if __name__ == '__main__':
    unittest.main()
