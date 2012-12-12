#!/usr/bin/env python

import popen2
import re
import shelve

import stats



def parse_counts(results, errors):
  counts = {}

  for line in results:
    m = errors.match(line)
    if m:
      stat = m.groups()[0]
      if stat not in counts: counts[stat] = 0
      counts[stat] += 1

  return counts



def produce_samples(counts, samples):
  for kind, count in counts.items():
    s = samples.get(kind, stats.Stats())
    s.sample(count)
    samples[kind] = s
  return samples



def load_history(path):
  return shelve.open(path)

def save_history(db):
  db.sync()
  db.close()



def print_stats(samples):
  for kind, stats in samples.items():
    print kind, " Count:", stats.count
    print " Min:", stats.min, " Max:", stats.max,
    print " Standard Deviation:", stats.standard_deviation,
    print " Mean:", stats.mean



def printed_errors(results):
  return re.compile(r'.*:.*:\s*([a-z]+):')



def c_make_results(block):
  cmd = 'make %s' % " ".join( block )
  print 'Running: ', cmd

  out, input = popen2.popen4(cmd)
  results = out.readlines()
  return results



def collect(block):
  history = load_history('samples.history')
  results = c_make_results(block)
  print "\n".join(results)
  errors  = printed_errors(results)
  counts  = parse_counts(results, errors)
  samples = produce_samples(counts, history)
  print_stats(samples)
  save_history(history)
