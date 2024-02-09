import json
import csv
import openpyxl
from datetime import datetime
import os
class ExcelWriter:
    def __init__(self, filename):
        self.filename = filename
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active

    def write_data(self, data):
        for row in data:
            self.sheet.append(row)

    def save(self):
        self.workbook.save(self.filename)

def convert_json_to_csv():
    json_file = os.path.join(os.path.dirname(__file__), "list.json")
    csv_file = os.path.join(os.path.dirname(__file__), datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv")

    with open(json_file, 'r') as file:
        data = json.load(file)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())  # Write header row
        for item in data:
            writer.writerow(item.values())

if __name__ == "__main__":
    json_file = "list.json"
    csv_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    convert_json_to_csv()
