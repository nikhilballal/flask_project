from flask import Flask,render_template
from data import Articles # function from data.py
# from module flask, we import the function Flask
app = Flask(__name__)

Articles = Articles() #create a variables equal to the function 'Articles' so that it can return the variable ' articles'

@app.route("/")   #without this, we will get 'not found' page.
def hello():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articles")
def articles():
    return render_template("articles.html" , articles = Articles) # since we want not only the html file, but also the data inside

@app.route("/article/<string:id>/") #pass in string of values containing a parameter 'id'
def article(id):
    return render_template("article.html" , id=id)


if __name__ == '__main__':
    app.run(debug = True) # so that we donot have to re-start the server







#  to push a code in github from terminals
# 1. git status
# 2. git add {File_Name} //the file name you haven been changed
# 3. git status
# 4. git commit -m '{your_message}'
# 5. git push origin master
