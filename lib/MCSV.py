import csv

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

if __name__ == '__main__':
  print read_at_indices("test.txt", 1)

def parse_dictionary(filename):
  results = {}
  with open(filename, 'r') as f:
    for l in f:
      for kv in l.split(", "):
        for k, v in kv.split("="):
          results.setdefault(k, []).append(try_number(v))
  return results
