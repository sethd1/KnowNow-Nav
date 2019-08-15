# this file should not be named 'flask.py', creates a name conflict that prevents flask from importing correctly - Joshua

from flask import Flask, render_template, url_for, redirect, request
import csv
import pandas as pd
app = Flask(__name__)



@app.route('/')
@app.route('/home')
def home():  
    return render_template('home.html')

@app.route('/form') # Input from html
def form():
    if request.method == 'GET':
        query = request.args['query']
        if query is not None:
            return redirect(url_for('searchForInsights', query=query))

@app.route('/results/<string:posts>')   # dictionary is not a valid route converter type, need to change - Joshua
def results(posts): 
	return render_template('SearchEngine.html',posts =posts) # sends output to html

@app.route('/search/<string:query>')
def searchForInsights(query):
    dictionary = {}
    with open('Patient Insights.csv') as f:
        r = csv.reader(f, delimiter=',')
        count = 0
        for row in r:
            count+=1
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
                    dictionary['Category tags'] = categoryTags
            if ';' not in categoryTags:
                dictionary['Category tags'] = categoryTags
            if query.title() in dictionary['Topic']:
                return redirect(url_for('results', posts = dictionary))
			
def associate_header_with_insights(header: str, entered_search: str) -> list: # Anne's code -- Capable of inputting any header -> Outputs dictionary
    with open('Finalized Cohort - Sheet1.csv', 'r', newline="") as f:     # This function requires two inputs: A header type and the search.
                                                                              # I wasn't sure how this would fit with the html inputs so the parameters may be incorrect
        patient_insights_list = []

        reader = csv.DictReader(f)
        data = list(reader) 
        headers = reader.fieldnames
    
        for dictionary in data:
            if entered_search.strip() in dictionary[header]:
                new_dict = {}

                new_dict[dictionary[header]] = dictionary['Patient insight']
                patient_insights_list.append(new_dict)

    return redirect(url_for('results', posts = patient_insights_list))
				
if __name__ == '__main__':
	app.run(debug=True)
