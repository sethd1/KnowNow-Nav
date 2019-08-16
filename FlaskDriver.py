# !/usr/bin/env python

"""FlaskDriver

If the description is long, the first line should be a short summary of FlaskDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from flask import Flask, render_template, url_for, redirect, request
from Spreadsheet import Spreadsheet

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
    'Patient insight':'insight',
    'Volunteers':'volunteers',
    'Discussion URL':'url',
    'Notes/ comments/ questions':'comments',
    "Smruti Vidwans comments/ Topics": 'professor_comment'}

__author__ = "Mauricio Lomeli"
__date__ = "8/15/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__license__ = "MIT"
__version__ = "#version"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


app = Flask(__name__)
app.config["DEBUG"] = True

sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)


def normalizeDict(items):
    dictionary = {}
    for


@app.route("/")
@app.route("/home")
def home():
    return render_template("Homepage.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        query = request.form('submit')
        if query is not None:
            return redirect(url_for('search', query=query))
    else:
        query = request.args.get('search_field')
        if query is not None:
            return redirect(url_for('search', query=query))


@app.route('/search/<string:query>')
def search(query):
    post = sheet[query]
    if len(post) > 0:
        dictionaries = []
        for item in post:
            dictionaries.append(dict(item))
        return redirect(url_for('results', posts=dictionaries))
    else:
        return redirect(url_for('results', posts=[]))


app.run()


