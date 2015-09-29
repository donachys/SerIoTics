import sys
import rethinkdb as r
import os
import subprocess
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
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).min('time').default(default_response).run(connection)['time']
def getStopTime(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).max('time').default(default_response).run(connection)['time']
def getRecordCount(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).sum('count').default(0).run(connection)
def computeRecordsPerSecond(start_time, end_time, num_records):
    time_diff = end_time-start_time
    if time_diff > 0:
        return num_records/(end_time-start_time)
    else:
        return 0
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
def graph():
    return render_template('graph.html')
@app.route('/api/json_throughput')
def json_throughput():
    jsonresponse = {"records_per_second": getRecordsPerSecond('json_test')}
    return jsonify(result = jsonresponse)
@app.route('/api/json_run/<execute>')
def json_run(execute):
    if(execute):
        cmd = ["bash","json_start.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        cmd = ["bash","json_stop.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
