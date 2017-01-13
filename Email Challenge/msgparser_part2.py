#!/usr/bin/env python

import tarfile
import csv
import sys
import os


def parse(f, terms, results):
    '''
    Parse the MSG header information.
    Takes parameters: file object, list of search terms, dictionary of results
    Header delimiter: '\n'
    Content delimiter: ': '
    '''
    path, name = os.path.split(f.name)
    for line in f:
        # Delimiter for end of header block
        if line == '\n':
            break
        # Compare header item name to terms we are extracting
        headerName = line.split(": ", 1)[0]
        if headerName in terms:
            # Extract content and store
            headerContent = line.split(": ", 1)[1].rstrip()
            results[name][headerName] = headerContent


def saveContentToFile(results, terms):
    '''Save parsed header content to CSV.'''
    with open('part2_results.csv', 'wb') as outfile:
        # Use dict writer to un-nest dictionarys
        fields = ['filename'] + terms
        writer = csv.DictWriter(outfile, fields)
        writer.writeheader()
        # Iterate over dictionaries and write out
        for filename, terms in results.items():
            row = {'filename': filename}
            row.update(terms)   # merge the dictionaries into a single row
            writer.writerow(row)


if __name__ == '__main__':
    # Sanitize user input
    if len(sys.argv) < 2:
        print "USAGE: python msgparser_part2.py [TAR Archive Path]"
        sys.exit()
    # Parse files without having to unpack the tarfile
    tar = tarfile.open(str(sys.argv[1]))
    terms = ['Date', 'From', 'Subject']
    results = dict()

    for member in tar.getmembers():
        f = tar.extractfile(member)   # extract read-only file
        if f is not None:
            # Strip the path from the file name
            path, name = os.path.split(f.name)
            results[name] = dict()
            parse(f, terms, results)

    saveContentToFile(results, terms)
