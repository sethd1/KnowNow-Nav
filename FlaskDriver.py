# !/usr/bin/env python

"""FlaskDriver

If the description is long, the first line should be a short summary of FlaskDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from flask import Flask, render_template, url_for, redirect, request, session
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
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


app = Flask(__name__)
app.config["DEBUG"] = True

sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)


@app.route("/")
@app.route("/home")
def home():
    """
    Renders the homepage. While the program is running, if a user
    enters 'localhost:5000/' into their web browser, they'll be
    rerouted to the homepage: Homepage.html
    :return:
    """
    return render_template("Homepage.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    Renders the results page. While the program is running, if a user
    submits/enters a dropdown menu selection, then enters the submission.
    This function activates and sends the info stored in the 'posts' variable
    to the ResultsPage.html.
    :return:
    """
    if request.method == 'POST':
        query = request.form('query')
    else:
        query = request.args.get('query')
    if query is None:
        print("You changed the name of the select list! Change it back to query.")
    posts = sheet[query]
    if len(posts) > 0:
        return render_template("ResultsPage.html", posts=posts)
    else:
        return render_template("ResultsPage.html")


app.run()


