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
#connection to rethinkDB
def createNewConnection():
    return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
#completion time of first micro-batch
def getStartTime(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).min('time').default(default_response).run(connection)['time']
#completion time of last micro-batch
def getStopTime(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).max('time').default(default_response).run(connection)['time']
#sum of all records computed during experiment
def getRecordCount(RDB_TABLE, connection):
    return r.table(RDB_TABLE).filter(r.row['count'].gt(0)).sum('count').default(0).run(connection)
#average throughput computation
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
#clear the table specified
def emptyTable(RDB_TABLE):
    connection = createNewConnection()
    r.table(RDB_TABLE).delete().run(connection)
    connection.close()
#routing for website
@app.route('/')
@app.route('/index')
def index():
    title = "SerIoTics"
    return render_template("index.html", title = title)
@app.route('/blog')
def blog():
    title = "SerIoTics"
    return render_template("blog.html", title = title)
#back-up pdf version of slides
@app.route('/slides_pdf')
def slides_pdf():
    return app.send_static_file('Shaun_Donachy_Demo.pdf')
@app.route('/exp_mp4')
def exp_mp4():
    return app.send_static_file('JSON_Avro_ProtoBuf.mp4')
#end points for animated demo
#commented out for paranoia
# @app.route('/super_secret/json_demo')
# def json_demo():
#     emptyTable('json_test')
#     return render_template('json_demo.html')
# @app.route('/api/json_throughput')
# def json_throughput():
#     jsonresponse = {"records_per_second": getRecordsPerSecond('json_test')}
#     return jsonify(result = jsonresponse)
# @app.route('/api/json_run/<execute>')
# def json_run(execute):
#     if(execute == "true"):
#         cmd = ["bash","json_start.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","json_stop.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     else:
#         return None
# @app.route('/api/json_run_producer/<execute>')
# def json_run_producer(execute):
#     if(execute == "true"):
#         cmd = ["bash","json_start_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","json_stop_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     else:
#         return None

# @app.route('/super_secret/avro_demo')
# def avro_demo():
#     emptyTable('avro_test')
#     return render_template('avro_demo.html')
# @app.route('/api/avro_throughput')
# def avro_throughput():
#     jsonresponse = {"records_per_second": getRecordsPerSecond('avro_test')}
#     return jsonify(result = jsonresponse)
# @app.route('/api/avro_run/<execute>')
# def avro_run(execute):
#     if(execute == "true"):
#         cmd = ["bash","avro_start.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","avro_stop.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     else:
#         return None
# @app.route('/api/avro_run_producer/<execute>')
# def avro_run_producer(execute):
#     if(execute == "true"):
#         cmd = ["bash","avro_start_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","avro_stop_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     else:
#         return None

# @app.route('/super_secret/proto_demo')
# def proto_demo():
#     emptyTable('protobuf_test')
#     return render_template('proto_demo.html')
# @app.route('/api/proto_throughput')
# def proto_throughput():
#     jsonresponse = {"records_per_second": getRecordsPerSecond('protobuf_test')}
#     return jsonify(result = jsonresponse)
# @app.route('/api/proto_run/<execute>')
# def proto_run(execute):
#     if(execute == "true"):
#         cmd = ["bash","proto_start.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","proto_stop.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
# @app.route('/api/proto_run_producer/<execute>')
# def proto_run_producer(execute):
#     if(execute == "true"):
#         cmd = ["bash","proto_start_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     elif(execute == "false"):
#         cmd = ["bash","proto_stop_prod.sh"]
#         p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
#                                 stderr=subprocess.PIPE,
#                                 stdin=subprocess.PIPE)
#         out,err = p.communicate()
#         return out
#     else:
#         return None

