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

#PySpark App to consume data from kafka, deserialize, and perform a map-reduce aggregation 
# on the unique device_id included in the message and sum the quantity in the message

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

    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    #delete any data in table
    connection = createNewConnection()
    r.table(RDB_TABLE).delete().run(connection)
    connection.close()
    
    streams = []
    #avro schema/reader
    schema = avro.schema.parse(open("/home/ubuntu/SerIoTics/Avro_consumer/WaterSensor.avsc").read())#absolute path =/
    reader = DatumReader(schema)
    numStreams = 6 #read parallelism
    #set up kafkaStreams into a list
    kafkaStreams = [KafkaUtils.createStream(ssc=ssc, zkQuorum=zkQuorum, groupId="Avro-consumer", valueDecoder=io.BytesIO, topics={topic: 1}) for _ in range (numStreams)]
    def sendRDDCount(count):
        connection = createNewConnection()
        r.table(RDB_TABLE).insert(count).run(connection)
        connection.close()
    def bytesDecoder(x):
        decoder = BinaryDecoder(x)
        return reader.read(x, decoder)

    for idx,kvs in enumerate(kafkaStreams):
        countsDstream=kvs.count()
        countsDstream = countsDstream.map(lambda x: {"count":x, "time":time.time()})
        records = kvs.map(lambda x: bytesDecoder(x[1]))
        sums = records.map(lambda obj: (obj['unique_id'], obj['quantity'])) \
            .reduceByKey(lambda a, b: a+b)
        countsDstream.foreachRDD(lambda rdd: sendRDDCount(rdd.take(1)))

    ssc.start()
    ssc.awaitTermination()