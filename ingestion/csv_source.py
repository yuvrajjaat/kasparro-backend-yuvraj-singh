import csv

class CSVIngestor:
    def fetch(self):
        with open("data/sample.csv") as f:
            return list(csv.DictReader(f))
