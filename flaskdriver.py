# !/usr/bin/env python

"""flaskdriver

Connects Cohort information from the spreadsheets with the front-end.
"""

import csv
from pathlib import Path
from flask import Flask, render_template, url_for, redirect, request

PATH = Path.cwd()

__author__ = "Derek Eijansantos"
__authors__ = "Derek Eijansantos, Jennifer Kwon, Anne Wang"
__date__ = "8/15/2019"
__credits__ = ["Mauricio Lomeli"]
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Derek Eijansantos"
__status__ = "Prototype"

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('SearchEngine.html')  # I am not entirely sure what is supposed to be on the home page.


@app.route('/form', methods=['GET', 'POST'])  # Input from html
def form():
    if request.method == 'GET':
        query = request.form('search_field')
        if query is not None:
            return redirect(url_for('search', query=query))
    else:
        query = request.args.get('search_field')
        if query is not None:
            return redirect(url_for('search', query=query))


@app.route('/results/<dictionary:posts')
def results(posts):
    return render_template('SearchEngine.html', posts=posts)  # sends output to html


@app.route('/search/<string:query>')
def searchForInsights(query):  # Jennifer's code -- Inputs Topic -> Outputs dictionary
    dictionary = {}
    with open('Patient Insights.csv') as f:
        r = csv.reader(f, delimiter=',')
        count = 0
        for row in r:
            count += 1
            topic = row[0].strip()
            topic = topic.title()
            dictionary['Topic'] = topic
            insight = row[7].strip()
            dictionary['Patient insight'] = []
            dictionary['Patient insight'].append(insight)
            categoryTags = row[5].strip()
            dictionary['Category tags'] = []
            if ';' in categoryTags:
                tagList = categoryTags.split('; ')
                for t in tagList:
                    dictionary['Category tags'].append(t)
            if ';' not in categoryTags:
                dictionary['Category tags'] = categoryTags
            if query.title() in dictionary['Topic']:
                return redirect(url_for('results', posts=dictionary))


def associate_header_with_insights(header: str,
                                   entered_search: str) -> list:  # Anne's code -- Capable of inputting any header -> Outputs dictionary
    with open('Finalized Cohort - Sheet1.csv', 'r',
              newline="") as f:  # This function requires two inputs: A header type and the search.​                                                                             # I wasn't sure how this would fit with the html inputs so the parameters may be incorrect
        patient_insights_list = []
        reader = csv.DictReader(f)
        data = list(reader)
        headers = reader.fieldnames
        for dictionary in data:
            if entered_search.strip() in dictionary[header]:
                new_dict = {}
                new_dict[dictionary[header]] = dictionary['Patient insight']
                patient_insights_list.append(new_dict)
    return redirect(url_for('results', posts=patient_insights_list))


if __name__ == '__main__':
    app.run(debug=True)
