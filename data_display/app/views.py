import sys
import rethinkdb as r
import os
import io

from flask import jsonify 
from flask import render_template
from flask import Flask

from app import app

RDB_HOST =  os.environ.get('RDB_HOST')
RDB_PORT = os.environ.get('RDB_PORT')
RDB_DB = "SerIoTics"
def createNewConnection():
    return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
def getStartTime(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).min('time').run(connection)['time']
def getStopTime(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).max('time').run(connection)['time']
def getRecordCount(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).sum('count').run(connection)
def computeRecordsPerSecond(start_time, end_time, num_records):
    return num_records/(end_time-start_time)
def getRecordsPerSecond(RDB_TABLE):
    connection = createNewConnection()
    start = getStartTime(RDB_TABLE, connection)
    stop = getStopTime(RDB_TABLE, connection)
    count = getRecordCount(RDB_TABLE, connection)
    connection.close()
    return computeRecordsPerSecond(start, stop, count)

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
    return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
@app.route('/api/json_throughput')
def json_throughput():
    jsonresponse = {"records_per_second": getRecordsPerSecond('json_test')}
    return jsonify(result = jsonresponse)
