import re
from lxml import etree

def monthNumber(month):
  month_numbers = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, \
                   'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12, \
                    'late': 12, 'summer': 7}
  if (month.isnumeric() == True): return month
  month = month.lower()
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
    if self.datePositions[dateItem] == 42: return 1
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
      s = re.sub('\?', '', s)
      s = re.sub(r'–', '-', s)
      tables = re.findall( r'<table.*?</table>', s)

      for x in range(0, 15):
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
  dateFormats.append(DateRangeFormat(r'^(\d+).* ([A-Za-z]+).* (\d+ ?\w+) - (\d+).* ([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 1, 'sm': 2, 'sy': 3, 'ed': 4, 'em': 5, 'ey': 6}))
  # 1 January - 28 March 193
  dateFormats.append(DateRangeFormat(r'^(\d+).* ([A-Za-z]+).* - (\d+).* ([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 1, 'sm': 2, 'sy': 5, 'ed': 3, 'em': 4, 'ey': 5}))
  # 20 March 235 - June 238
  dateFormats.append(DateRangeFormat(r'^(\d+).* ([A-Za-z]+).* (\d+ ?\w+) - ([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 1, 'sm': 2, 'sy': 3, 'ed': 42, 'em': 4, 'ey': 5}))
  # March 22, 238 - April 12, 238
  dateFormats.append(DateRangeFormat(r'^([A-Za-z]+).* (\d+),.* (\d+ ?\w+) - ([A-Za-z]+).* (\d+),.* (\d+ ?\w+)', \
    {'sd': 2, 'sm': 1, 'sy': 3, 'ed': 2, 'em': 1, 'ey': 3}))
  # February 244 - September/October 249
  dateFormats.append(DateRangeFormat(r'^([A-Za-z]+).* (\d+ ?\w+) - ([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 42, 'sm': 1, 'sy': 2, 'ed': 42, 'em': 3, 'ey': 4}))
  # October 253 - 260
  dateFormats.append(DateRangeFormat(r'^([A-Za-z]+).* (\d+ ?\w+) - (\d+ ?\w+)', \
    {'sd': 42, 'sm': 1, 'sy': 2, 'ed': 42, 'em': 42, 'ey': 3}))
  # September 275
  dateFormats.append(DateRangeFormat(r'^([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 42, 'sm': 1, 'sy': 2, 'ed': 42, 'em': 1, 'ey': 2}))
  # 383/384 - August 28, 388
  dateFormats.append(DateRangeFormat(r'(\d+ ?\w+) - ([A-Za-z]+).* (\d+), (\d+ ?\w+)', \
    {'sd': 42, 'sm': 42, 'sy': 1, 'ed': 3, 'em': 2, 'ey': 4}))
  # '407/409 - August or September 411'
  dateFormats.append(DateRangeFormat(r'(\d+ ?\w+) - ([A-Za-z]+).* (\d+ ?\w+)', \
    {'sd': 42, 'sm': 42, 'sy': 1, 'ed': 42, 'em': 2, 'ey': 3}))
  parseFile('./parser/data.data', dateFormats)