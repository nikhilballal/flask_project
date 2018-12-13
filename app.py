from flask import Flask
app = Flask(__name__)

@app.route("/") #decorator
def hello():
	return "Hello World!"

@app.route("/about")
def about():
	return "I am Ballal"

@app.route("/about/contact")
def contact():
	return "phone number"

lalalalalalalalala


if __name__=='__main__':
	app.run()	



