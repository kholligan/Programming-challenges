import unittest
import msgparser_part2


class MSGTests(unittest.TestCase):
    def test_parse_contents(self):
        with open('./Test_Email/test_msg_attachment.txt', 'r') as infile:
            test_terms = ['Date', 'From', 'Subject']
            test_expected_result = {
                    'test_msg_attachment.txt':
                    {
                        'Date': "Tue, 10 Jan 2017 14:24:31 -0700",
                        'From': "Test Account <returnpath.test.kevin@gmail.com>",
                        'Subject': "Home depot with attachment"
                    }
                }

            result = dict()
            result['test_msg_attachment.txt'] = dict()
            msgparser_part2.parse(infile, test_terms, result)
            self.assertEqual(test_expected_result, result)

if __name__ == '__main__':
    unittest.main()
