from flask import Flask
from flask import render_template

import scripts

app = Flask(__name__)

# Home page route
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/generic')
def generic():
	return render_template('generic.html')

@app.route('/search', methods = ['POST'])
def search_query():
	pass
	# Do Something

# User Search Page Route
@app.route('/user/<username>')
def user_page(username):
	userdata = scripts.getUserInfo(username)
	return userdata
	#return "User %s" % username

# App route sample Post
@app.route('/get/', methods = ['GET', 'POST'] )
def test():
	print "Test"

if __name__ == '__main__':
	app.debug = True
	app.run()