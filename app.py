from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import Articles # function from data.py
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# from module flask, we import the function Flask
app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'myflaskproject'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  #queries in mysql can return dictionaries

#initialize MYSQL
mysql = MySQL(app)

# Articles = Articles() #create a variables equal to the function 'Articles' so that it can return the variable ' articles'.

#Index
@app.route("/")   #without this, we will get 'not found' page.
def index():
    return render_template('home.html')
#About
@app.route("/about")
def about():
    return render_template("about.html")

#Articles
@app.route("/articles")
def articles():
        #Create cursor
        cur = mysql.connection.cursor()

        #Get articles
        result = cur.execute("SELECT * FROM articles")

        articles = cur.fetchall()

        if result> 0:
            return render_template('articles.html', articles = articles)
        else:
            msg = 'No Articles Found'
            return render_template('articles.html', msg=msg)
        #Close connection
        cur.close()

#Single Article
@app.route("/article/<string:id>/") #pass in string of values containing a parameter 'id'
def article(id):
            #Create cursor
            cur = mysql.connection.cursor()

            #Get articles
            result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

            article = cur.fetchone()
            return render_template("article.html" , article=article)


#Register Form Classssss
class RegisterForm(Form):
    name= StringField('Name', [validators.Length(min=1, max=50)])
    username =  StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message= 'Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

#User Register
@app.route('/register', methods=['GET','POST'])
def register():

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",(name,email,username,password))

        #commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
#to check if it is GET or POST request, and  make sure it is all validated
    return render_template('register.html', form=form) # since we want not only the html file, but also the data inside

#User Login
@app.route('/login', methods=['GET','POST']) #to get both GET and POST requests
def login():
    if request.method == 'POST':
        #get Form Fields
        username = request.form['username']
        password_candidate = request.form['password'] #password_candidate ,want the correct password that we get from the database and compare with one typed on the form

        # create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate,password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

            #close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

#Check if user logged in. To avoid unauthorized login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear() #kill the session
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
@is_logged_in  #indicate that this is page that the user has to be logged into.
def dashboard():
    #Create cursor
    cur = mysql.connection.cursor()

    #Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result> 0:
        return render_template('dashboard.html', articles = articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

    #Close connection
    cur.close()

#Article Form Class
class ArticleForm(Form):
    title= StringField('Title', [validators.Length(min=1, max=200)])
    body =  TextAreaField('Body', [validators.Length(min=30)])

#Add Article
@app.route('/add_article', methods= ['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        #Create Cursor
        cur = mysql.connection.cursor()

        #execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        #commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)



if __name__ == '__main__':
    app.secret_key ='pass' #set a secret key for password fail
    app.run(debug = True) # so that we donot have to re-start the server







#  to push a code in github from terminal
# 1. git status
# 2. git add {File_Name} //the file name you changed
# 3. git status
# 4. git commit -m '{your_message}'
# 5. git push origin master
