import matplotlib.pyplot as plt
import matplotlib
import MCSV
import MList
import re
import time

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

def parse_datetime(date_string):
  ds, ms = date_string.replace("[", "").replace("]", "").split(".", 1)
  return time.mktime(time.strptime(ds, "%Y%m%d-%H:%M:%S")) + float("."+ms)

def plot_values(output_name, value_list, xlabel=None, ylabel=None, title=None, linetype='k', xoffset=0):
  plt.clf()
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel is not None:
    plt.ylabel(ylabel)
  if title is not None:
    plt.title(title)

  xlist = range(xoffset, len(value_list)+xoffset)

  plt.plot(xlist, value_list, linetype)
  plt.savefig(parse_output_name(output_name))

def sliding_window(value_list, window_size=10):
  out_values = []
  cumulative = 0.0
  for i, v in enumerate(value_list):
    cumulative += v
    if window_size <= i:
      out_values.append(cumulative / window_size)
      cumulative -= value_list[i - window_size + 1]
  return out_values

def plot_hist(output_name, value_list, bins=100, xlabel=None, ylabel=None, title=None, linetype='k'):
  plt.clf()
  if xlabel is not None:
    plt.xlabel(xlabel)
  if ylabel is not None:
    plt.ylabel(ylabel)
  if title is not None:
    plt.title(title)

  plt.hist(value_list, bins=bins)

if __name__ == "__main__":
  # values = MCSV.read_at_indices("../cache_misses_120712.txt", 2)[2]
  # plot_values("../cache_misses_120712", values, xlabel=r"$10^6$'s of accesses", ylabel="Cumulative miss rate", title=r"lru, cachesize $10^6$, randomwalk($10^4$ steps, depth 2)")

  # values = MCSV.read_at_indices("../rw_misses_120712.txt", 0)[0]
  # plot_values("../rw_misses_120712", values, xlabel=r"$10^6$'s of users", ylabel="Miss Rate for this random walk", title=r"lru, cachesize $10^6$, randomwalk($10^4$ steps, depth 2)")
  
  # values = MCSV.read_at_indices("../cache_misses_120718_10m_10m_const.txt", 2)[2]
  # plot_values("../cache_misses_120718_10m_10m_const", values, xlabel=r"$10^7$'s of accesses", ylabel="Cumulative miss rate", title=r"lru, cachesize $10^7$ const, randomwalk($10^4$ steps, depth 2)")

  # values = MCSV.read_at_indices("../cache_misses_120718_100m_10m.txt", 2)[2]
  # plot_values("../cache_misses_120718_100m_10m", values, xlabel=r"$10^7$'s of accesses", ylabel="Cumulative miss rate", title=r"lru, cachesize $10^8$ const, randomwalk($10^4$ steps, depth 2)")

  dates = [parse_datetime(dt) for dt in MCSV.read_at_indices("../guavacache_100m.txt", 1)[1]]
  diffs = MList.diffs(dates)
  plot_values("../guavacache_100m", sliding_window(diffs, 200), 
    xlabel=r"# of personalizations", ylabel="Time (s)", 
    title=r"Compute Rate (guava, cachesize $10^8$ const, randomwalk($10^4$ steps, depth 2))", xoffset=200)