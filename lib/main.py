import matplotlib.pyplot as plt
import matplotlib
import MCSV
import re

def colors(length):
  colors=[]
  c = matplotlib.cm.get_cmap('gist_rainbow')
  for i in range(length):
    colors.append(c(1.*i/length))
  return colors

def parse_output_name(output_name):
  if re.search("\.[a-zA-Z0-9]{2,3}$", output_name):
    return output_name
  else:
    return output_name + ".png"

def plot_values(output_name, value_list, xlabel=None, ylabel=None, title=None, linetype='k'):
  plt.clf()
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel is not None:
    plt.ylabel(ylabel)
  if title is not None:
    plt.title(title)

  xlist = range(0, len(value_list))

  plt.semilogx(xlist, value_list, linetype)
  plt.savefig(parse_output_name(output_name))

if __name__ == "__main__":
  values = MCSV.read_at_indices("../cache_misses_120712.txt", 2)[2]
  plot_values("../cache_misses_120712", values, xlabel=r"$10^6$'s of accesses", ylabel="Miss Rate", title=r"lru, cachesize $10^6$, randomwalk($10^4$ steps, depth 2)")