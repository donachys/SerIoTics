from __future__ import print_function

import sys
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import rethinkdb as r
import json
import os


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: SparkStreamingKafkaJSONSumRDB.py <zk> <topic> <window size (sec)> <tablename>", file=sys.stderr)
        exit(-1)

    RDB_HOST =  os.environ.get('RDB_HOST')
    RDB_PORT = os.environ.get('RDB_PORT')
    RDB_DB = "SerIoTics"
    zkQuorum, topic, stream_window, RDB_TABLE = sys.argv[1:]
    stream_window = int(stream_window)
    
    sc = SparkContext(appName="PythonStreamingKafkaJSONSums")
    ssc = StreamingContext(sc, batchDuration=stream_window)
    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    #delete any data in table
    connection = createNewConnection()
    r.table(RDB_TABLE).delete()
    connection.close()
    
    streams = []
    
    numStreams = 6
    kafkaStreams = [KafkaUtils.createStream(ssc, zkQuorum, "JSON-consumer", {topic: 1}) for _ in range (numStreams)]

    def sendRDDCount(count):
        connection = createNewConnection()
        r.table(RDB_TABLE).insert({"count": count, "time":time.time()}).run(connection)
    def sendPartitionCount(index, count):
        connection = createNewConnection()
        r.table(RDB_TABLE).insert({"partition":index, "count": count, "time":time.time()}).run(connection)
        connection.close()
    def sendPartition(iter):
        connection = createNewConnection()
        for record in iter:
            r.table(RDB_TABLE).insert(json.loads(record[1])).run(connection)
        connection.close()
    for idx,kvs in enumerate(kafkaStreams):
        records = kvs.map(lambda x: json.loads(x[1]))
        count = records.count()
        sums = records.map(lambda obj: (obj['unique_id'], obj['quantity'])) \
            .reduceByKey(lambda a, b: a+b)
        kvs.foreachRDD(lambda rdd: sendRDDCount(count))

    ssc.start()
    ssc.awaitTermination()