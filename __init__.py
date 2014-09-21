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

@app.route('/search', methods = ['GET'])
def search_query():
	q = request.args.get("q")
	if q is None:
		return redirect(url_for('home'))
	else : 		
		page = request.args.get("p")
		return json.dumps(scripts.findData(q))
		#return "Search for " + q

# User Search Page Route
@app.route('/user/<username>')
def user_page(username):
	userdata = scripts.getUserInfo(username)
	print userdata
	return render_template('user.html', user = userdata)
	#return "User %s" % username

# App route sample Post
@app.route('/get/', methods = ['GET', 'POST'] )
def test():
	print "Test"

if __name__ == '__main__':
	app.debug = True
	app.run()