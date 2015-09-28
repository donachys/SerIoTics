#changes are highlighted in blue

from flask import jsonify 
from flask import render_template
from flask import Flask
#jsonify creates a json representation of the response
from app import app

#change the bolded text to the keyspace which has the table you want to query. Same as above for < or > and quotations. In this case, it will be playground.
@app.route('/')
def homepage():

    title = "SerIoTics"
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
@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('index2.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)