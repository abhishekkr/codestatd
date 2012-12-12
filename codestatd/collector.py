#

import popen2
import re

import data_handler
import stats


def parse_counts(results, errors):
  counts = {}
  success = 'true'

  for line in results:
    m = errors.match(line)
    if m:
      success = 'false'
      stat = m.groups()[0]
      if stat not in counts: counts[stat] = 0
      counts[stat] += 1
  if success=='true': counts['error'] = 0
  return counts



def produce_samples(counts, samples):
  for kind, count in counts.items():
    s = samples.get(kind, stats.Stats())
    s.sample(count)
    samples[kind] = s
  return samples



def print_samples(samples_path):
  samples = data_handler.load_history(samples_path)
  for kind, stats in samples.items():
    print "\n", kind, " Count:", stats.count
    print " Min:", stats.min, " Max:", stats.max,
    print " Standard Deviation:", stats.standard_deviation,
    print " Mean:", stats.mean
  data_handler.save_history(samples)



def printed_errors(results):
  return re.compile(r'.*:.*:\s*([a-z]+):')



def c_make_results(block):
  cmd = 'make %s' % " ".join( block )
  print 'Running: ', cmd

  out, input = popen2.popen4(cmd)
  results = out.readlines()
  return results



def collect(block, samples_path):
  history = data_handler.load_history(samples_path)
  results = c_make_results(block)
  print "\n".join(results)
  errors  = printed_errors(results)
  counts  = parse_counts(results, errors)
  samples = produce_samples(counts, history)
  data_handler.save_history(history)
