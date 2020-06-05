import re
from lxml import etree

def monthNumber(month):
  month_numbers = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, \
                   'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
  if (month.isnumeric() == True): return month
  return month_numbers[month]
class DateRangeFormat:
  def __init__(self, dateFormat, datePositions):
    self.dateFormat = dateFormat
    self.datePositions = datePositions

  def parseDateRange(self, dateRange):
    self.match = re.search(self.dateFormat, dateRange)
    # Just for debug
    self.dateRange = dateRange
    return self.match != None

  def getDateItem(self, dateItem):
    if dateItem == 'sd' or dateItem == 'ed':
      return int(self.match.group(self.datePositions[dateItem]))
    if dateItem == 'sm' or dateItem == 'em':
      return monthNumber(self.match.group(self.datePositions[dateItem]))
    if dateItem == 'sy' or dateItem == 'ey':
      year = self.match.group(self.datePositions[dateItem])
      annoDomini = True
      if (year.endswith('BC')):
        annoDomini = False
        year = year[0:-2]
      if (year.endswith('AD')):
        annoDomini = True
        year = year[0:-2]
      year = int(year.strip())
      if not annoDomini: year *= -1
      return year
    return None

def parseDateRange(dateRange, dateFormats):
  for dateFormat in dateFormats:
    if not dateFormat.parseDateRange(dateRange): continue
    startDate = {'d': dateFormat.getDateItem('sd'), 'm': dateFormat.getDateItem('sm'), 'y': dateFormat.getDateItem('sy')}
    endDate = {'d': dateFormat.getDateItem('ed'), 'm': dateFormat.getDateItem('em'), 'y': dateFormat.getDateItem('ey')}
    return [startDate, endDate]
  raise Exception("Can't find suitable format for date: {}".format(dateRange)) 


def parseFile(filename, dateFormats):
  with open(filename, encoding="utf8") as data_file:
      s = data_file.readline()
      s = re.sub(r'<a.*?href="(.*?)".*?>(.*?)</a>', r'\2 {\1}', s)
      tables = re.findall( r'<table.*?</table>', s)

      for x in range(0, 4):
        table = etree.HTML(tables[x]).find("body/table")
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        if not headers: continue
        for row in rows:
            values = [col.text for col in row]
            tleader = dict(zip(headers, values))
            leader = dict()
            leader['nameLatin'] = tleader['Name']
            parsedDate = parseDateRange(tleader['Reign'], dateFormats)
            leader['start'] = parsedDate[0]
            leader['end'] = parsedDate[1]
            print(leader)

if __name__ == "__main__":
  dateFormats = []
  dateFormats.append(DateRangeFormat(r'^(\d+).* ([A-Za-z]+).* (\d+ ?\w+) – (\d+).* ([A-Za-z]+).* (\d+ ?\w+)$', \
    {'sd': 1, 'sm': 2, 'sy': 3, 'ed': 4, 'em': 5, 'ey': 6}))
  dateFormats.append(DateRangeFormat(r'^(\d+).* ([A-Za-z]+).* – (\d+).* ([A-Za-z]+).* (\d+ ?\w+)$', \
    {'sd': 1, 'sm': 2, 'sy': 5, 'ed': 3, 'em': 4, 'ey': 5}))
  parseFile('./parser/data.data', dateFormats)