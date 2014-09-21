from flask import Flask
from flask import render_template
import json
from flask import request, redirect, url_for

import scripts

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generic')
def generic():
	return render_template('about.html')

@app.route('/map')
def map():
	return render_template('map.html')

@app.route('/search', methods = ['GET'])
def search_query():
	q = request.args.get("q")
	if q is None:
		return redirect(url_for('home'))
	else : 		
		page = request.args.get("p")
		results = json.dumps(scripts.searchData(q,10))
		#return results
		return render_template('results.html', q = q, results = scripts.searchData(q,10))

# Return 100 results for a keyword for anaysis
@app.route('/keyword/<keyword>')
def get_keyword(keyword):
	return json.dumps(scripts.searchData(keyword,100))

# User Search Page Route
@app.route('/user/<username>')
def user_page(username):
	userdata = scripts.getUserInfo(username)

	return render_template('user.html', user = userdata[0], feedback = userdata[1])
	#return json.dumps(userdata)

# App route sample Post
@app.route('/get/', methods = ['GET', 'POST'] )
def test():
	print "Test"

if __name__ == '__main__':
	app.debug = True
	app.run()