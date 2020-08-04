from app.Calculator.Calculator import Calculator
from app.Statistics.Median import median
from app.Statistics.Mode import mode
from app.Statistics.StandardDeviation import stddev
from app.Statistics.Variance import variance


class Statistics(Calculator):
    data = []

    def __init__(self):
        super().__init__()

    def median(self, data):
        self.result = median(data)
        return self.result

    def mode(self, data):
        self.result = mode(data)
        return self.result

    def stddev(self, data):
        self.result = stddev(data)
        return self.result

    def variance(self, data):
        self.result = variance(data)
        return self.result

    pass
