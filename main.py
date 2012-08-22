import MCSV
import re
import time
import os.path
from mtools import *
from mtools import mplot

def parse_datetime(date_string):
  ds, ms = date_string.replace("[", "").replace("]", "").split(".", 1)
  return time.mktime(time.strptime(ds, "%Y%m%d-%H:%M:%S")) + float("."+ms)


def plot_metrics(name):
  dicty = MCSV.parse_dictionary("data/%s.txt" % name)
  mplot.one.p('plots/%s_average.png' % name, dicty['average'], sliding=100)
  mplot.one.p('plots/%s_sum.png' % name, dicty['sum'], sliding=100)
  return dicty


def plot_metrics_compare(metric, name1, name2, title='', twoscales=False):
  if name2 < name1: name1, name2 = name2, name1
  diry = "plots/comparisons/%s/%s" % (name1, name2)
  if not os.path.exists(diry):
    os.makedirs(diry)
  dicty1 = MCSV.parse_dictionary("data/%s.txt" % name1)
  dicty2 = MCSV.parse_dictionary("data/%s.txt" % name2)
  if twoscales:
    mplot.two.scales('%s/%s.png' % (diry, metric),
      dicty1[metric], dicty2[metric], title=title, sliding=100, labels=[name1, name2])
  else:
    mplot.two.p('%s/%s.png' % (diry, metric),
      dicty1[metric], dicty2[metric], title=title, sliding=100, labels=[name1, name2])


def plot_comparison_metrics(name1, name2, twoscales=False):
  plot_metrics_compare("average", name1, name2, title="Average Time", twoscales=twoscales)
  plot_metrics_compare("sum", name1, name2, title="Sum (Total Time)", twoscales=twoscales)
  plot_metrics_compare("count", name1, name2, title="Count", twoscales=twoscales)


def plot_guava_metrics(name):
  ne = MCSV.read_at_indices("data/%s.txt" % name, 0, 1, 2, 3)
  if not os.path.exists("plots/%s" % name):
    os.makedirs("plots/%s" % name)
  # Misses per node
  miss_diff, acc_diff = mgroup.list.diffs(ne[0]), mgroup.list.diffs(ne[1])
  mplot.one.p('plots/%s/misses' % name, miss_diff, title='Misses per PTC', sliding=1000)
  # Miss rate per node
  miss_rate_diff = [ (a - 0.0)/b if b > 0 else 0.0 for a, b in zip(miss_diff, acc_diff)]
  mplot.one.p('plots/%s/miss_rate' % name, miss_rate_diff, title='Miss rate per PTC', sliding=1000)
  # Cumulative miss rate
  mplot.one.p('plots/%s/miss_rate_cum' % name, ne[2], title='Cumulative miss rate', sliding=1000)
  # Guava Average Load Penalty
  mplot.one.p('plots/%s/avg_load_penalty_cum' % name, ne[3], title='Cumulative average load penalty', sliding=1000)

def plot_cache_metrics(name):
  ne = MCSV.read_at_indices("data/%s.txt" % name, 0, 1, 2, 3, 4)
  if not os.path.exists("plots/%s" % name):
    os.makedirs("plots/%s" % name)
  nodes, edges = ne[3], ne[4]
  # Cumulative nodes/edges in the cache
  mplot.two.scales('plots/%s/nodes_edges_cum.png' % name, nodes, edges,
    title='Cumulative Nodes and Edges in the Cache', sliding=100, labels=['Nodes', 'Edges'])
  # Misses per node
  miss_diff, acc_diff = mgroup.list.diffs(ne[0]), mgroup.list.diffs(ne[1])
  mplot.one.p('plots/%s/misses' % name, miss_diff, title='Misses per PTC', sliding=1000)
  # Miss rate per node
  miss_rate_diff = [ (a - 0.0)/b if b > 0 else 0.0 for a, b in zip(miss_diff, acc_diff)]
  mplot.one.p('plots/%s/miss_rate' % name, miss_rate_diff, title='Miss rate per PTC', sliding=1000)
  # Cumulative miss rate
  mplot.one.p('plots/%s/miss_rate_cum' % name, ne[2], title='Cumulative miss rate', sliding=1000)

if __name__ == "__main__":
  # # Comparing PTC across cache sizes
  # plot_comparison_metrics("ptc_lru_2b10m", "ptc_lru_4b20m")

  # # Comparing PTC across cache types
  # plot_comparison_metrics("ptc_lru_2b10m", "ptc_gua_2b10m")
  # plot_comparison_metrics("ptc_lru_2b10m", "ptc_clo_2b10m")
  # plot_comparison_metrics("ptc_gua_2b10m", "ptc_clo_2b10m")

  # # Comparing cache misses and disk reads
  # plot_comparison_metrics("flr_lru_2b10m", "esr_lru_2b10m")
  # plot_comparison_metrics("flr_lru_4b20m", "esr_lru_4b20m")

  # # Compare PTC and cache misses
  # plot_comparison_metrics("ptc_lru_2b10m", "flr_lru_2b10m", True)
  # plot_comparison_metrics("ptc_lru_4b20m", "flr_lru_4b20m", True)

  # # Plot nodes and edges in cache over time
  # # Plot # of misses per random walk over time
  # plot_cache_metrics("lru_2b10m_nodes")
  # plot_cache_metrics("lru_4b20m_nodes")
  # plot_cache_metrics("clo_2b10m_nodes")
  # plot_guava_metrics("gua_2b10m_nodes")

  # Get time and counts
  # dicty = MCSV.parse_dictionary("data/delta_ptc_1343933720.txt")
  # times = [parse_datetime(d) for d in dicty['time']]
  # counts = dicty['count']
  # dicty2 = MCSV.parse_dictionary("data/delta_esr_1343933720.txt")
  # times2 = [parse_datetime(d) for d in dicty2['time']]
  # counts2 = dicty2['count']
  # mplot.two.scales('plots/test', [times, counts], [times2, counts2], title='PTC Count over time', labels=['PTC Count', 'Disk Read Count'], sliding=1000)

  # freqpairs = MCSV.parse_piggy('data/all_accs_dist_20120807/part-r-00000')
  # mplot.one.loglog('plots/freqpairs', freqpairs, xlabel='Access Count', ylabel='Frequency')

  prac = MCSV.read_at_indices_limit('data/all_users_pagerank_20120821/part-r-00000', 10000, 20000, 1, 3)
  mplot.two.scales('plots/pagerank_accesses_10k_20k', prac[1], prac[3], labels=['Accesses', 'PageRank'], sliding=1000)
  prac = MCSV.read_at_indices_limit('data/all_users_pagerank_20120821/part-r-00000', 0, 10000, 1, 3)
  mplot.two.scales('plots/pagerank_accesses_0k_10k', prac[1], prac[3], labels=['Accesses', 'PageRank'], sliding=1000)

