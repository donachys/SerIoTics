#changes are highlighted in blue

from flask import jsonify 
from flask import render_template
from flask import Flask
#jsonify creates a json representation of the response
from app import app

#change the bolded text to the keyspace which has the table you want to query. Same as above for < or > and quotations. In this case, it will be playground.
@app.route('/')
def homepage():

    title = "Epic Tutorials"
    paragraph = ["Wow, a website homepage"]

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception, e:
        return str(e)
@app.route('/index')
def index():
   user = { 'nickname' : 'Miguel' } #fake user detected!
   mylist = [1,2,3,4]
   return render_template("index.html", title = 'Home', user = user, mylist = mylist)
