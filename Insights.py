# !/usr/bin/env python

"""Insights

If the description is long, the first line should be a short summary of Insights.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import csv

PATH = Path.cwd()
DEFAULT_SPREADSHEET = "Patient Insights - Insights.csv"

__author__ = "Mauricio Lomeli"
__date__ = "8/15/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class insights:
    def __init__(self, spreadsheet=DEFAULT_SPREADSHEET):
        self.headers = None
        self.spreadsheet = []
        self.__index = 0
        if spreadsheet is not None:
            self.assemble(spreadsheet)

    def assemble(self, spreadsheet):
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            self.headers = content.fieldnames
            self.spreadsheet = [element for element in content]

    def getColumn(self, fieldname):
        return [item[fieldname] for item in self.spreadsheet if fieldname in item]

    def find(self, value):
        results = []
        for row in self.spreadsheet:
            if value in row.values():
                results.append(row)
        return results

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in self.headers:
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


