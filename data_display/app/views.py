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
default_response = {"time":0}
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
def emptyTable(RDB_TABLE):
    connection = createNewConnection()
    r.table(RDB_TABLE).delete().run(connection)
    connection.close()

@app.route('/')
@app.route('/index')
def index():
    title = "SerIoTics"
   return render_template("index.html", title = title)
@app.route('/super_secret/json_demo')
def json_demo():
    emptyTable('json_test')
    return render_template('json_demo.html')
@app.route('/api/json_throughput')
def json_throughput():
    jsonresponse = {"records_per_second": getRecordsPerSecond('json_test')}
    return jsonify(result = jsonresponse)
@app.route('/api/json_run/<execute>')
def json_run(execute):
    if(execute == "true"):
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
@app.route('/api/json_run_producer/<execute>')
def json_run_producer(execute):
    if(execute == "true"):
        cmd = ["bash","json_start_prod.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        cmd = ["bash","json_stop_prod.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out

@app.route('/super_secret/avro_demo')
def avro_demo():
    emptyTable('avro_test')
    return render_template('avro_demo.html')
@app.route('/api/avro_throughput')
def avro_throughput():
    jsonresponse = {"records_per_second": getRecordsPerSecond('avro_test')}
    return jsonify(result = jsonresponse)
@app.route('/api/avro_run/<execute>')
def avro_run(execute):
    if(execute == "true"):
        cmd = ["bash","avro_start.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        cmd = ["bash","avro_stop.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
@app.route('/api/avro_run_producer/<execute>')
def avro_run_producer(execute):
    if(execute == "true"):
        cmd = ["bash","avro_start_prod.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        cmd = ["bash","avro_stop_prod.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out

