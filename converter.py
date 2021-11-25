import re
import json

def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))

raw = open("raw.txt", encoding="utf-8")
lines = raw.readlines()
russianLines = []
finnishLines = []
for line in lines:
  if(has_cyrillic(line)):
    russianLines.append(line)
  else:
    finnishLines.append(line)
i = 0
newDictionary =  {}
for russianLine in russianLines:
  finnishLine = finnishLines[i]
  newDictionary[finnishLine.replace("\n", "")] = russianLine.replace("\n", "")
  i += 1
with open('newDict.json', 'w', encoding='utf-8') as file:
    json.dump(newDictionary, file, ensure_ascii=False)
