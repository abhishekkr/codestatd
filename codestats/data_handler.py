#

import shelve
import csv
import time

def load_history(path):
  return shelve.open(path)

def save_history(db):
  db.sync()
  db.close()

def save_to_csv(samples_path, csv_path):
  samples = load_history(samples_path)
  csv_samples = csv.writer(open(csv_path, 'a+'))
  for kind, stats in samples.items():
    csv_samples.writerow([time.time(), kind, stats.count, stats.sum, stats.sum_square, stats.min, stats.max, stats.standard_deviation, stats.mean])
    del samples[kind]
  save_history(samples)
