from flask import Flask,render_template
# from module flask, we import the function Flask
app = Flask(__name__)

@app.route("/")   #without this, we will get 'not found' page.
def hello():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug = True) # so that we donot have to re-start the server
