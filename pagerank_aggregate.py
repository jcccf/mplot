import glob
from collections import defaultdict

minval = 3.4691095476199285E-10
maxval = 8.342083379429959E-4  
numbins = 10000
binsize = (maxval - minval) / 10000

bins = defaultdict(int)
for filename in glob.glob("part-*"):
  with open(filename, 'r') as f:
    for l in f:
      value = float(l.split("\t")[1]) - minval
      bins[int(value/binsize)] += 1

with open("pagerank_bins_%f.txt" % binsize, 'w') as f:
  for k, v in sorted(bins.iteritems()):
    f.write("%d\t%d\n" % (k, v))
