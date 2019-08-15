from flask import Flask, render_template, url_for, redirect, request
import csv
import pandas as pd
app = Flask(__name__)



@app.route('/')
@app.route('/home')
def home():
    return render_template('SearchEngine.html') # I am not entirely sure what is supposed to be on the home page.

@app.route('/form', methods = ['GET', 'POST']) # Input from html
def form():
	if request.method == 'GET':
		query = request.form('search_field')
		if query is not None:
			return redirect(url_for('search',query =query))
	else: 
		query = request.args.get('search_field')
		if query is not None:
			return redirect(url_for('search',query =query))

@app.route('/results/<dictionary:posts')
def results(posts): 
	return render_template('SearchEngine.html',posts =posts) # sends output to html

@app.route('/search/<string:query>')
def searchForInsights(query): # Jennifer's code -- Outputs dictionary
	dictionary = {}
	with open('Patient Insights.csv') as f:
		r = csv.reader(f, delimiter = ',')
		count = 0
		for row in r:
			count+=1
			topic = row[0].strip()
			topic = topic.title()
			dictionary['Topic'] = topic
			insight = row[7].strip()
			dictionart['Patient insight'] = []
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
				return redirect(url_for('results', posts = dictionary))
				
if __name__ == '__main__':
	app.run(debug=True)