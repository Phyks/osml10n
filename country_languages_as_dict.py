#!/usr/bin/python3

print("country_languages = {")
ha=''
with open("country_languages.data.in") as cl:
  i=0
  for line in cl:
    if (line[0] == '#'):
      continue
    list=line.strip().split('\t')
    langs=list[1].strip('{''}').split(',')
    country=list[0]
    ha=ha+("'%s':%s, " % (country,langs))
    if i==7:
      ha=ha+"\n"
      i=0
    i+=1
ha=ha.strip(','' ')
print(ha)
print('}')



