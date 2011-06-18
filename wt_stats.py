#!/usr/bin/python
import sys
from collections import defaultdict

from entrypoint import entrywithfile
from wiktionary import is_form_of

def normalise_pos(pos):

    if "{{initialism" in pos:
        return "{{initialism}}"

    if "{{abbreviation" in pos:
        return "{{abbreviation}}"

    if "{{acronym" in pos:
        return "{{acronym}}"

    return pos.strip(" 123456")

@entrywithfile('utf8', tsv='r', output='w')
def main(tsv, date, output, progress=False):
    """
        Creates the statistics from the tsv wiktionary dump

        tsv: The latest tsv file of definitions
	output: The destination file for stats
        date: The date of the last dump
        --progress -p: Display progress?
    """
    gloss = defaultdict(lambda: 0)
    nongloss = defaultdict(lambda: 0)
    pages = defaultdict(set)

    total=0

    for line in tsv:
        language, page, section, defn = line.split("\t",3)

        pages[language].add(page)

        if is_form_of(defn):
            nongloss[language] += 1
        else:
            gloss[language] += 1

        total += 1

        if progress:
            if not total % 10000:
                print >>sys.stderr, ".",

    count,incount = 0,0
    rows = []
    for language in sorted(pages):
        count += 1

        if len(pages[language]) >= 10:
            incount += 1

            rows.append((language, len(pages[language]), nongloss[language] + gloss[language], gloss[language], nongloss[language]))

        rowformat = u"""|-
! %s
|| %s || %s || %s || %s"""
    
    table = u"\n".join(rowformat % row for row in rows)

    print >>output, u"""
'''Warning:''' This information is inexact. It comes from an XML dump file dated '''%s''', however the dump may not have been accurate at the time. It uses some guesswork to distinguish form-of entries and requests for definitions, this may divide things incorrectly.

Of the '''%s''' languages on Wiktionary, only the '''%s''' with 10 or more entries are shown.

There are approximately '''{{FORMATNUM:%s}}''' definitions in total. <!-- Or how I count them this time anyway... -->
{| class="sortable prettytable"
! Language name || Number of entries || Number of definitions || Gloss definitions || Form-of definitions
""" % (date, count, incount, total)

    print >>output, table
    print >>output, "|}"
