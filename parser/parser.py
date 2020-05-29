import re
from lxml import etree

with open('data.txt', encoding="utf8") as data_file:
    s = data_file.readline()
    tables = re.findall( r'<table.*?</table>', s)

    for x in range(0, len(tables)):
      table = etree.HTML(tables[x]).find("body/table")
      rows = iter(table)
      headers = [col.text for col in next(rows)]
      for row in rows:
          values = [col.text for col in row]
          print(dict(zip(headers, values)))
          print("================================")
