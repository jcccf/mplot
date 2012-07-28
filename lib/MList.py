
def diffs(listy):
  diffitems = []
  previtem = listy[0]
  for l in listy:
    diffitems.append(l - previtem)
    previtem = l
  return diffitems[1:]
