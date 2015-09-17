name := "ConsumeKafka-SubmitCass"

version := "1.0"

scalaVersion := "2.10.4"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.4.1" % "provided",
	"org.apache.spark" %% "spark-sql" % "1.3.0" % "provided",
	"org.apache.spark" % "spark-streaming_2.10" % "1.3.0" % "1.5.0",
	"org.apache.spark" % "spark-streaming-kafka_2.10" % "1.3.0",
	"com.datastax.spark" %% "spark-cassandra-connector" % "1.5.0-M1"
)

mergeStrategy in assembly := {
  case m if m.toLowerCase.endsWith("manifest.mf")          => MergeStrategy.discard
  case m if m.toLowerCase.matches("meta-inf.*\\.sf$")      => MergeStrategy.discard
  case "log4j.properties"                                  => MergeStrategy.discard
  case m if m.toLowerCase.startsWith("meta-inf/services/") => MergeStrategy.filterDistinctLines
  case "reference.conf"                                    => MergeStrategy.concat
  case _                                                   => MergeStrategy.first
}
