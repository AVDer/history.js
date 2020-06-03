import re
from lxml import etree

def monthNumber(month):
  month_numbers = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, \
                   'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
  if (month.isnumeric() == True): return month
  return month_numbers[month]

def parseDate(date, dateFormats):
  date = date.strip()
  ad = True
  if (date.endswith('BC')):
    ad = False
    date = date[0:-2]
  if (date.endswith('AD')):
    ad = True
    date = date[0:-2]
  date = date.strip()
  components = date.split(' ')
  if (len(components) == 3):
    return {'d': int(components[0]), 'm': monthNumber(components[1]), 'y': ('' if ad else '-') + str(int(components[2]))}
  return date


def parseDateRange(range, dateSplitter, dateFormats):
  dates = range.split(dateSplitter)
  return (parseDate(dates[0], dateFormats), parseDate(dates[1], dateFormats))


def parseFile(filename, dateSplitter, dateFormats):
  result = []
  with open(filename, encoding="utf8") as data_file:
      s = data_file.readline()
      s = re.sub(r'<a.*?href="(.*?)".*?>(.*?)</a>', r'\2 {\1}', s)
      tables = re.findall( r'<table.*?</table>', s)

      for x in range(0, 1):
        table = etree.HTML(tables[x]).find("body/table")
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        for row in rows:
            values = [col.text for col in row]
            tleader = dict(zip(headers, values))
            leader = dict()
            leader['nameLatin'] = tleader['Name']
            parsedDate = parseDateRange(tleader['Reign'], dateSplitter, dateFormats)
            leader['start'] = parsedDate[0]
            leader['end'] = parsedDate[1]
            print(leader)

if __name__ == "__main__":
  parseFile('./parser/data.data', '–', 'd M Y')