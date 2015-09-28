from __future__ import print_function

import sys
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter, BinaryDecoder

import rethinkdb as r
import json
import os
import io

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: SparkStreamingKafkaAvroSumRDB.py <zk> <topic> <window size (sec)> <tablename>", file=sys.stderr)
        exit(-1)

    RDB_HOST =  os.environ.get('RDB_HOST')
    RDB_PORT = os.environ.get('RDB_PORT')
    RDB_DB = "SerIoTics"
    zkQuorum, topic, stream_window, RDB_TABLE = sys.argv[1:]
    stream_window = int(stream_window)
    
    sc = SparkContext(appName="PythonStreamingKafkaAvroSums")
    ssc = StreamingContext(sc, batchDuration=stream_window)

    
    streams = []
    schema = avro.schema.parse(open("WaterSensor.avsc").read())
    reader = DatumReader(schema)
    numStreams = 4

    kafkaStreams = [KafkaUtils.createStream(ssc=ssc, zkQuorum=zkQuorum, groupId="Avro-consumer", valueDecoder=io.BytesIO, topics={topic: 1}) for _ in range (numStreams)]
    def sendRDDCount(count):
        connection = createNewConnection()
        r.table(RDB_TABLE).insert({"count": count, "time":time.time()}).run(connection)
        connection.close()
    def sendPartitionCount(index, count):
        connection = createNewConnection()
        r.table(RDB_TABLE).insert({"partition":index, "count": count, "time":time.time()}).run(connection)
        connection.close()
    def sendPartition(iter):
        connection = createNewConnection()
        for record in iter:
            r.table(RDB_TABLE).insert(json.loads(record[1])).run(connection)
        connection.close()
    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    def bytesDecoder(x):
        decoder = BinaryDecoder(x)
        return reader.read(x, decoder)

    for idx,kvs in enumerate(kafkaStreams):
        records = kvs.map(lambda x: bytesDecoder(x[1]))
        sums = records.map(lambda obj: (obj['unique_id'], obj['quantity'])) \
            .reduceByKey(lambda a, b: a+b)
        kvs.foreachRDD(lambda rdd: sendRDDCount(rdd.count()));

    ssc.start()
    ssc.awaitTermination()