# used in collector

from math import sqrt

class Stats(object):

  def __init__(self, sum=0.0, sum_square=0.0, count=0, min=0.0, max=0.0):
    self.sum        = sum
    self.sum_square = sum_square
    self.count      = count
    self.min        = min
    self.max        = max

  def sample(self, size):
    self.sum        += size
    self.sum_square += size * size

    if self.count == 0:
      self.min = size
      self.max = size
    else:
      if self.min > size: self.min = size
      if self.max < size: self.max = size

    self.count += 1.0

  def get_mean(self):
    try:
      return self.sum / self.count
    except ZeroDivisionError:
      return 0.0

  def get_standard_deviation(self):
    try:
      return sqrt(
        ( self.sum_square - ( self.sum * self.sum / self.count)
        ) / ( self.count -1 )
      )
    except ZeroDivisionError:
      return 0.0

  mean = property(get_mean)
  standard_deviation = property(get_standard_deviation)
