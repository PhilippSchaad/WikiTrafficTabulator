import datetime, csv, json, urllib, httplib2
from urllib.request import urlopen
names = list()
years = ["2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
base_url = "http://stats.grok.se/json/de/"
with open('names.csv', 'r', encoding="ISO-8859-1") as file:
    reader = csv.reader(file)
    for line in reader:
        for item in line:
            if item != '':
                names.append(item)
for year in years:
    y_url = base_url + year
    data = [list() for _ in range(len(names))]
    i = 0
    for name in names:
        data[i].append(name + "(" + year + ")")
        for month in months:
            url = y_url + month + "/" + name
            url = httplib2.iri2uri(url)
            print(url)
            datJson = json.loads(urlopen(url).read().decode("utf-8"))
            if len(datJson['daily_views']) > 0:
                for entry in datJson['daily_views']:
                    try:
                        datetime.datetime.strptime(entry, '%Y-%m-%d')
                        data[i].append(entry + ": " + str(datJson['daily_views'][entry]))
                    except ValueError:
                        pass
        i += 1
    for l in data:
        l[1:] = sorted(l[1:], key=lambda x: datetime.datetime.strptime(x.rsplit(':', 1)[0], '%Y-%m-%d'))
    data = list(zip(*data))
    with open("out/" + year + ".csv", 'w+') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)
