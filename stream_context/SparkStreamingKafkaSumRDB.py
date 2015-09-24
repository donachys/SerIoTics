from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import rethinkdb as r
import json
import os


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: SparkStreamingKafkaSumRDB.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    RDB_HOST =  os.environ.get('RDB_HOST')
    RDB_PORT = os.environ.get('RDB_PORT')
    RDB_DB = "mytopic2db"
    RDB_TABLE = "test2"
    sc = SparkContext(appName="PythonStreamingKafkaSums")
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic = sys.argv[1:]
    streams = []
    
    numStreams = 4
    kafkaStreams = [KafkaUtils.createStream(ssc, zkQuorum, "my-topic2-consumer", {topic: 1}) for _ in range (numStreams)]
    #kvs = kafkaStreams[1]
    #kkvvss = ssc.union(*kafkaStreams)#.partitionBy(numPartitions=20)
    #kvs.print()


    #kvs = KafkaUtils.createStream(ssc, zkQuorum, "my-topic2-consumer", {topic: 1})
    def sendPartitionCount(index, count):
        #print('index: ' + str(index))
        connection = createNewConnection()#todo: use-connection-pool
        #print('count' + str(count))
        r.table(RDB_TABLE).filter(r.row["partition"] == index).update({"count": count}).run(connection)
        connection.close()
    def sendPartition(iter):
        connection = createNewConnection()#todo: use-connection-pool
        for record in iter:
            #    r.table(RDB_TABLE).insert(record).run(connection)
            #print(record[1])
            r.table(RDB_TABLE).insert(json.loads(record[1])).run(connection)
        connection.close()
    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    
    #kvs.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))
    #"rdds: "+str(kvs.count()).pprint()
    def printParts(time, rdd):
            print("-------##########################----------")
            print(rdd.getNumPartitions())
            print("-------##########################----------")
    kafkaStreams[0].foreachRDD(lambda rdd: sendPartitionCount(0,rdd.count()))
    kafkaStreams[1].foreachRDD(lambda rdd: sendPartitionCount(1,rdd.count()))
    kafkaStreams[2].foreachRDD(lambda rdd: sendPartitionCount(2,rdd.count()))
    kafkaStreams[3].foreachRDD(lambda rdd: sendPartitionCount(3,rdd.count()))
    #kkvvss.foreachRDD(lambda rdd: sendPartitionCount(0,rdd.count()))
    for idx,kvs in enumerate(kafkaStreams):
        #kvs.foreachRDD(printParts)
        records = kvs.map(lambda x: json.loads(x[1]))
        sums = records.map(lambda obj: (obj['unique_id'], obj['quantity'])) \
            .reduceByKey(lambda a, b: a+b)
        #sums.pprint(num=300)
        #kvs.count().pprint()
    #kkvvss.foreachRDD(printParts)
    #records = kkvvss.map(lambda x: json.loads(x[1]))
    #sums = records.map(lambda obj: (obj['unique_id'], obj['quantity'])) \
    #    .reduceByKey(lambda a, b: a+b)
    #sums.pprint(num=10)

    ssc.start()
    ssc.awaitTermination()