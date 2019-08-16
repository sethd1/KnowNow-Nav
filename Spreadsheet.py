# !/usr/bin/env python

"""Spreadsheet

If the description is long, the first line should be a short summary of Spreadsheet.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import csv

PATH = Path.cwd()
DEFAULT_SPREADSHEET = "Patient Insights - Insights.csv"
NORM_HEADERS = {
    'Topic': 'topic',
    'Date discussion (month/ year)':'date',
    'Patient Query/ Inquiry':'query',
    'Specific patient profile':'profile',
    'Patient cohort (definition)':'cohort',
    'Category tag':'category',
    'Secondary tags':'secondary',
    'Patient insight':'insights',
    'Volunteers':'volunteers',
    'Discussion URL':'url',
    'Notes/ comments/ questions':'comments',
    "Smruti Vidwans comments/ Topics": 'professor_comments'}


__author__ = "Mauricio Lomeli"
__date__ = "8/15/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class Spreadsheet:
    def __init__(self, spreadsheet=DEFAULT_SPREADSHEET, headers=NORM_HEADERS):
        self.real_headers = None
        self.norm_headers = None
        self.spreadsheet = []
        self.__index = 0
        if spreadsheet is not None:
            self.assemble(spreadsheet)
        if headers is not None:
            self.normalize(headers)

    def assemble(self, spreadsheet):
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            self.real_headers = content.fieldnames
            self.spreadsheet = [element for element in content]

    def getColumn(self, fieldname):
        return [item[fieldname] for item in self.spreadsheet if fieldname in item]

    def find(self, value):
        results = []
        for row in self.spreadsheet:
            if value in row.values():
                results.append(row)
        return results

    def normalize(self, headers):
        self.norm_headers = headers.values()
        sheet = []
        for row in self.spreadsheet:
            dictionary = {}
            for key, value in row.items():
                dictionary[headers[key]] = value
            sheet.append(dictionary)
        self.spreadsheet = sheet

    def __getitem__(self, item):
        if isinstance(item, str):
            if self.norm_headers is not None and item in self.norm_headers:
                return self.getColumn(item)
            if item in self.real_headers:
                return self.getColumn(item)
            else:
                return self.find(item)
        elif isinstance(item, tuple):
            pos1, pos2 = item
            if isinstance(pos1, str) and isinstance(pos2, str):
                return [element.values() for element in self.spreadsheet if element[pos1] == pos2]
            elif isinstance(pos1, int) and isinstance(pos2, str):
                return self.spreadsheet[pos1 - 1][pos2]
        elif isinstance(item, int):
            return self.spreadsheet[item]

    def __len__(self):
        return len(self.spreadsheet)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.spreadsheet):
            raise StopIteration
        item = self.spreadsheet[self.__index]
        self.__index += 1
        return item


