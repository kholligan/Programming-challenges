#Return Path Test Case Submission

##Build and Run
To run unit tests:
```
$python email_unittest.py
$python msg_unittest.py
```
The test files/gold files are stored in the folder /Test_Email/.

To run part 1:
```
$python emailsearch_part1.py
```
This will output `part1_results.csv`. The email credentials for the dummy GMail account are stored in the file.

To run part 2:
```
$python msgparser_part2.py [TAR Archive Path]
```
This will output `part2_results.csv`.

## Part 1: Search From Email
In this code section I made frequent use of the `imaplib` module from python's built-in IMAP4 protocol client. I used this module because it comes with a robust object/feature set and is easy to install, configure, and use. It is also in line with GMail's use of iMAP/POP emails.

### 1.1 Connect to the server
To connect to the server, we use `imaplib.IMAP_SSL('imap.gmail.com')`. This returns an SSLObject instance that we will use to perform all other actions. 

We use `login()` on the instance with the provided credentials (here we've hardcoded them for the purposes of this test, but would ordinarily discard them or store them using appropriate encryption). This will either return an authenticated instance or will throw an exception if it fails.

### 1.2 Search and retrieve
To retrieve mail from the server, we first `.select()` which mailbox we want to retrieve from and then supply the parameters of our search. In this instance, we've selected `[Gmail]/All Mail` as our mailbox as this allows us to pull from all mailboxes without iterating through them.

To search, traditionally, you would call `.search()`, however, this returns the sequential ID, which may change during execution. Instead, we want to use the unique ID (uid) in order to isolate mail messages without disrupting others. Thus, we use the `.uid()` method and supply the command as a parameter (i.e. `server.uid('search'...)`).
Search, paired with 'SUBJECT', will return all emails with the exact phrase located anywhere in the subject. It then returns the SID or UID of the raw email content which can be manipulated further. 
We use `.uid(fetch,...)` to retrieve the actual messages from the server, which returns them in tuples of message part envelope and data. 
We use python's email module, which handles MIME and RFC2822 based messages. This allows us to easily extract message contents from the header or body. We invoke this by by calling `email.message_from_string()`.

### 1.3 Output
I chose to save the results in CSV file format, and chose to store the UID, sender, recipient, date, and message body. We could have stored the entire contents as plain text or in some other format as well, but none of these were specified in the requirements. 
To store items in CSV, create a writer object using python's CSV module by calling `csv.writer([file object])`. Then we write the header and extract the content of the email message and store in rows. For this section, I used and credited code found on StackOverflow as it was not related to the requirements but helped complete my CSV file.

## Part 2: Parse MSG Archive
In this section we parse a MSG archive to retrieve the date, sender, and subject from the emails. 

### 2.1 Extract files from tar
We can parse the files from the tar archive without manually extracting them by using Python's tarfile module. THis allows us to call `.extractfile()`, which creates a read-only file object that we can parse information from.

### 2.2 Parse and store
By examining the patterns of the MSG files, we noticed that header information came first and was separated by a newline before message content. We also noticed that each header line item began with the name of the header item, followed by a colon, and then the associated information. Thus, we delimited our parser by those two key items.
We stored our data in a nested dictionary of format:
 `{'message name': {'date': ..., 'sender': ..., 'subject': ....}}`
 This allowed for easily storage, retrieval, or search on our temporary data. 

### 2.3 Output
We stored the results in CSV file format, as specified. We used a slightly different methodology than in 1.3, as we used a DictWriter instead of a Writer. This was used to expand our nested dictionary to have all content written to a single row. We used `csv.DictWriter()` and supplied our search terms as the fields. We then iterated over the dictionary and wrote our content to the file. 
