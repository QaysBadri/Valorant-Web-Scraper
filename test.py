import os
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from time import sleep

posd=defaultdict(list)
ratingd=defaultdict(int)
wind=defaultdict(int)

def process(act, page):
  req = requests.get(f"https://tracker.gg/valorant/leaderboards/ranked/all/ranked?platform=all&region=na&act={act}&type=ranked&page={page}")

  soup = BeautifulSoup(req.content, "html.parser")

  #print(soup.get_text())

  try:
    children = soup.select_one('.trn-table>tbody').children
    entries = [[s for s in c.get_text().replace(" ", "").splitlines() if s] for c in children]
    entries=list(filter(lambda l: len(l)==6,entries))
  except Exception:
    print(soup.get_text())
    print('retrying')
    sleep(3)
    process(act, page)
    return

  for i in range(len(entries)):
    pos,name,discrim,rating,title,wins=entries[i]
    name+=discrim
    pos=int(pos.replace(',',''))
    rating = int(rating.replace(',',''))
    wins=int(wins.replace(',',''))
    posd[name].append(pos)
    ratingd[name]+=rating
    wind[name]+=wins

acts=['97b6e739-44cc-ffa7-49ad-398ba502ceb0', 'ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff', '52e9749a-429b-7060-99fe-4595426a0cf7', '2a27e5d2-4d30-c9e2-b15a-93b8909a442c', '4cb622e1-4244-6da3-7276-8daaf1c01be2', 'a16955a5-4ad0-f761-5e9e-389df1c892fb', '573f53ac-41a5-3a7d-d9ce-d6a6298e5704', 'd929bc38-4ab6-7da4-94f0-ee84f8ac141e', '3e47230a-463c-a301-eb7d-67bb60357d4f']

for act in acts:
  for i in range(10):
    print(f'ACT {act} PAGE {i}')
    process(act, i+1)

l=list(map(lambda t: (t[1],t[0]),ratingd.items()))
l.sort(reverse=True)
for i in l:
  x, y = i
  print(y, "-", x)
