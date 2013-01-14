#

import shelve
import csv
import time

#
class DataShelve:
  def load_history(path):
    return shelve.open(path)

  def save_history(db):
    db.sync()
    db.close()

#
class DataCSV:
  def add_shelve_to_csv(shelve_path, csv_path):
    shelves = load_history(shelve_path)
    csv_samples = csv.writer(open(csv_path, 'a+'))
    for kind, stats in shelves.items():
      csv_samples.writerow([time.time(), kind, stats.count, stats.sum, stats.sum_square, stats.min, stats.max, stats.standard_deviation, stats.mean])
      del shelves[kind]
    save_history(shelves)
