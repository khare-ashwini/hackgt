from flask import Flask
from flask import render_template
app = Flask(__name__)

# Home page route
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/generic')
def generic():
	return render_template('generic.html')

# User Search Page Route
@app.route('/user/<username>')
def user_page():
	return "User %s" % username

# App route sample Post
@app.route('/get/', methods = ['GET', 'POST'] )
def test():
	print "Test"

if __name__ == '__main__':
	app.debug = True
	app.run()