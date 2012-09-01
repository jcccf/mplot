import csv
import re

def detect_delimiter(line):
  """Try to detect any possibe delimiters given a single line"""
  delimiter = " "
  if "\t" in line:
    delimiter = "\t"
  elif "," in line:
    delimiter = ","
  return delimiter

def try_number(s):
  """Attempt to convert a string into a number if possible"""
  try:
    return float(s)
  except ValueError:
    return s

def read_at_indices_limit(filename, start, end, *indices):
  results = {}
  with open(filename, 'r') as f:
    delimiter = detect_delimiter(f.readline())
    f.seek(0)
    reader = csv.reader(f, delimiter=delimiter)
    for j, row in enumerate(reader):
      if j >= start:
        for i in indices:
          results.setdefault(i, []).append(try_number(row[i]))
      if j > end:
        break
  return results  

def read_at_indices_sample(filename, sample_rate, *indices):
  results = {}
  with open(filename, 'r') as f:
    delimiter = detect_delimiter(f.readline())
    f.seek(0)
    reader = csv.reader(f, delimiter=delimiter)
    for j, row in enumerate(reader):
      if j % sample_rate == 0:
        for i in indices:
          results.setdefault(i, []).append(try_number(row[i]))
  return results

def read_at_indices(filename, *indices):
  """Return arrays of values at the given indices
  Ex. for a file "1.0 2.0 3.0\n4.0 5.0 6.0"
  read_at_indices("test.txt", 1, 2) will return
  { 1:[2.0, 5.0], 2:[3.0,6.0] }
  """
  results = {}
  with open(filename, 'r') as f:
    delimiter = detect_delimiter(f.readline())
    f.seek(0)
    reader = csv.reader(f, delimiter=delimiter)
    for row in reader:
      for i in indices:
        results.setdefault(i, []).append(try_number(row[i]))
  return results

def parse_dictionary(filename):
  results = {}
  with open(filename, 'r') as f:
    for l in f:
      if l.strip() == 'count=0':
        for k in results.keys():
          results[k].append(0.0)
      else:
        for kv in l.split(", "):
          k, v = kv.split("=")
          results.setdefault(k, []).append(try_number(v))
  return results

def parse_piggy(filename):
  with open(filename, 'r') as f:
    text = f.read()
    frequencies, cumulativehist = text.split(")},{(")
    frequencies = frequencies[3:]
    cumulativehist = cumulativehist[:-4]
    frequencypairs = [tuple(pair.split(",")) for pair in frequencies.split("),(")]
    cumulativehistpairs = cumulativehist.split("),(")
    return frequencypairs

if __name__ == '__main__':
  pass
  # parse_piggy('data/all_accs_dist_20120807/part-r-00000')
  # print parse_ranklist('data/all_accs_20120829/part-r-00000')