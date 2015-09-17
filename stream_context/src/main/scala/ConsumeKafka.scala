
import kafka.serializer.StringDecoder
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._

import com.datastax.spark.connector.streaming._

object ConsumeKafka {

 def main(args: Array[String]) {
    val appName = "ConsumeKafka-SubmitCassandra"
    val brokers = "ec2-54-153-26-178.us-west-1.compute.amazonaws.com:9092"
    val topics = "my-topic2"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName(appName)
    val ssc = new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)
    
    // Get the lines and show results
    messages.foreachRDD { rdd =>
        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._
        val lines = rdd.map(_._2)
        val ticksDF = lines.map( x => {
                                  val tokens = x.split(",")
                                  Tick(tokens(0).toInt, tokens(1), tokens(2), tokens(3), tokens(4).toDouble)}).toDF()
        val ticks_per_source_DF = ticksDF.groupBy("source_id")
                               .agg("quantity" -> "avg", "quantity" -> "sum")
                               .orderBy("source_id")
        ticks_per_source_DF.show()
        //ticks_per_source_DF.saveToCassandra("playground")
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()

 }
}
case class Tick(source_id: Int, item_sensed: String, subject_measured: String, sensor_location_name: String, quantity: Float)

/** Lazily instantiated singleton instance of SQLContext */

object SQLContextSingleton {

  @transient  private var instance: SQLContext = _

  def getInstance(sparkContext: SparkContext): SQLContext = {

    if (instance == null) {

      instance = new SQLContext(sparkContext)

    }

    instance

  }

}
