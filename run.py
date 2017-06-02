import datetime, csv, json, urllib, httplib2, re
import os.path
from urllib.request import urlopen
from sys import argv

articles = []
years = []
months = []
language = 'en'

def write_to_file(data, year):
    with open(''.join(['out/', year, '.csv']), 'w+') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)

def get_stat(year, month, page, language):
    data = []
    base_url = "http://stats.grok.se/json/"
    url = ''.join([base_url, language, '/', year, month, '/', page])
    url = httplib2.iri2uri(url)
    json_data = json.loads(urlopen(url).read().decode("utf-8"))
    if len(json_data['daily_views']) > 0:
        for day in json_data['daily_views']:
            try:
                datetime.datetime.strptime(day, '%Y-%m-%d')
                data.append(''.join(
                    [day, ': ', str(json_data['daily_views'][day])]))
            except ValueError:
                pass
    return data

def retrieve_data():
    for year in years:
        data = [[] for _ in range(len(articles))]
        i = 0
        for article in articles:
            data[i].append(''.join([article, "(", year, ")"]))
            for month in months:
                for day in get_stat(year, month, article, language):
                    data[i].append(day)
            i += 1
        for l in data:
            l[1:] = sorted(l[1:], key=lambda x: datetime.datetime.strptime(
                x.rsplit(':', 1)[0], '%Y-%m-%d'))
        data = list(zip(*data))
        write_to_file(data, year)

def load_articles_from_file(filename):
    with open(filename, 'r', encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        for line in reader:
            for item in line:
                if item != '':
                    articles.append(item)

def print_help():
    print("")
    print("-h    Print this help page")
    print("")
    print("-f    Usage [-f $filename], where $filename is the file name (with")
    print("      .csv) of the csv file containing the articles to tabulate")
    print("-n    Usage [-n $name], where $name is the article to tabulate")
    print("      (can't be used if -f is used)")
    print("")
    print("-y    Usage [-y YYYY], where YYYY is the year to tabulate")
    print("-r    Usage [-r 'yyyy, YYYY'], where yyyy represents the starting")
    print("      date, and YYYY the end date of the range")
    print("      (can't be used if -y is used)")
    print("")
    print("-l    Usage [-y lang], where lang is the code for the desired")
    print("      language, for example en, de, es... Default: en")
    print("")
    quit()

def bad_use(msg):
    print(msg)
    print_help()

def check_filename():
    i = argv.index('-f')
    if i >= len(argv) - 1:
        bad_use("Invalid use of -f")
    filename = argv[i + 1]
    if os.path.isfile(filename):
        load_articles_from_file(filename)
    else:
        bad_use(''.join(["Could not find file ", filename]))

def check_article():
    i = argv.index('-n')
    if i >= len(argv) - 1:
        bad_use("Invalid use of -n")
    artname = argv[i + 1]
    articles.append(artname)

def check_year():
    i = argv.index('-y')
    if i >= len(argv) - 1:
        bad_use("Invalid use of -y")
    raw_year = argv[i + 1]
    year = -1
    try:
        year = int(raw_year)
    except ValueError:
        bad_use("Invalid argument for year, try a 4 digit integer")
    if year < 2007 or year > datetime.datetime.now().year:
        bad_use("Year cannot be earlier than 2007 or in the future")
    years.append(str(year))
    for i in range(1, 13):
        months.append(str(i).zfill(2))

def check_range():
    i = argv.index('-r')
    if i >= len(argv) - 1:
        bad_use("Invalid use of -r")
    daterange = argv[i + 1]
    r = re.compile('\d{4}, \d{4}')
    if not r.match(daterange):
        bad_use("Invalid date range format, use 'yyyy, YYYY'")
    dates = re.finditer('\d{4}', daterange)
    s_date_range = next(dates)
    s_date_string = daterange[s_date_range.start():s_date_range.end()]
    e_date_range = next(dates)
    e_date_string = daterange[e_date_range.start():e_date_range.end()]
    try:
        s_date = datetime.datetime.strptime(s_date_string, '%Y').year
        e_date = datetime.datetime.strptime(e_date_string, '%Y').year
        if s_date == e_date:
            bad_use("Dates are equal. If you only want one year, use -y")
        elif s_date > e_date:
            bad_use("The starting date cannot be greater than the end date")
        elif s_date < 2007:
            bad_use("The starting date has to be 2007 or later")
        elif e_date > datetime.datetime.now().year:
            bad_use("The end date cannot be in the future")
        for year in range(s_date, e_date + 1):
            years.append(str(year))
        for i in range(1, 13):
            months.append(str(i).zfill(2))
    except ValueError:
        bad_use("Invalid dates")

def check_language():
    i = argv.index('-l')
    if i >= len(argv) - 1:
        bad_use("Invalid use of -l")
    language = argv[i + 1]

def parse_args():
    nargs = len(argv)
    if nargs <= 1:
        bad_use("No arguments specified")
    elif nargs == 2 and '-h' in argv:
        print_help()
    elif nargs == 5 or nargs == 7:
        if '-f' in argv:
            if '-n' in argv:
                bad_use("Invalid use of -n, -f already given")
            check_filename()
        elif '-n' in argv:
            if '-f' in argv:
                bad_use("Invalid use of -f, -n already given")
            check_article()
        else:
            bad_use("No articles specified, use -n or -f")

        if '-y' in argv:
            if '-r' in argv:
                bad_use("Invalid use of -r, -y already given")
            check_year()
        elif '-r' in argv:
            if '-y' in argv:
                bad_use("Invalid use of -y, -r already given")
            check_range()
        else:
            bad_use("No date specified, use -y or -r")

        if nargs == 7:
            if '-l' in argv:
                check_language()
            else:
                bad_use("Too many arguments, only use -f/n and -y/r (-l) or -h")
    else:
        bad_use("Too many arguments, only use -f/n and -y/r (-l) or -h")

# Entry
if __name__ == "__main__":
    parse_args()
    retrieve_data()
