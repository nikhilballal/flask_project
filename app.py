from flask import Flask,render_template, flash, redirect, url_for, session, logging, request
from data import Articles # function from data.py
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
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

class RegisterForm(Form):
    name= StringField('Name', [validators.Length(min=1, max=50)])
    username =  StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message= 'Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         return render_template('register.html')#to check if it is GET or POST request, and make sure it is all validated
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug = True) # so that we donot have to re-start the server







#  to push a code in github from terminals
# 1. git status
# 2. git add {File_Name} //the file name you haven been changed
# 3. git status
# 4. git commit -m '{your_message}'
# 5. git push origin master
