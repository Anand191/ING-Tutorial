name := "Scala-Spark"

version := "1.0"

scalaVersion := "2.11.11"

libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-core_2.11" % "2.1.1",
  "org.apache.spark" % "spark-sql_2.11" % "2.1.1",
  "org.apache.spark" % "spark-mllib_2.11" % "2.1.1",
  "org.apache.spark" % "spark-streaming_2.11" % "2.1.1",
  "org.apache.spark" % "spark-graphx_2.11" % "2.1.1"
)
        