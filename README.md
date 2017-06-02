# WikiTrafficTabulator
## Introduction
A script to retrieve Wikipedia article traffic statistics from stats.grok.se and tabulate them.

## Requirements
Requires Python 3.
Non standard Python packages used:
 - httplib2 (Install with `sudo pip install httplib2` or `sudo pip3 install httplib2`)

## Usage
Run the script with `python3 run.py`, providing following arguments:
 - To specify the articles to tabulate
   - use `-n` to specify the name of one individual article, or
   - use `-f` to specify the name of a CSV file containing multiple names of all articles
     to fetch (same format as names.csv)
 - To specify the year(s) to retrieve
   - use `-y` to specify one year
   - use `-r` to specify a range of years (`-r 'yyyy, YYYY'`, where yyyy is the starting
     year, and YYYY the end year (both inclusive))
 - Optionally, you can specify a language code with `-l` (e.g. `de` for german pages)

Wait for the script to complete

Find your results in the `out` folder

Every year has its own CSV file, where columns represent one article (e.g. `Siemens(2017)`),
and rows represent one day of the year, with the corresponding view count.
