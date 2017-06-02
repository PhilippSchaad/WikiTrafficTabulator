# WikiTrafficTabulator
## Introduction
A script to retrieve Wikipedia article traffic statistics from stats.grok.se and tabulate them.
Retrieves all data from 2007 up to and including 2015 on the german Wikipedia page entries.

## Requirements
Requires Python 3.
Non standard Python packages used:
 - httplib2 (Install with `sudo pip install httplib2` or `sudo pip3 install httplib2`)

## Usage
Provide the names of the (german) Wikipedia articles you want to query in a file called `names.csv`
in the root project folder (you can modify the existing one, making sure the format stays the same).

Run the script with `python3 run.py`, and wait for it to complete.

The output, in the form of one CSV file per year, gets placed in the `out` directory.

The output CSV files have a format, where every column represents an article (e.g. `Siemens(2006)`)
and every row represents a day of the year.
