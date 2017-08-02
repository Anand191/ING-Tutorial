/**
  * Created by anand on 7/12/17.
  */
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession
object file_reader {
  def test2(args:Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("File Reading Test")
    conf.setMaster("local[*]")
    val sc = new SparkContext(conf)
    println(sc)

    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.some.config.option", "some-value")
      .getOrCreate()
    val df = spark.read.format("com.databricks.spark.csv").option("header", "true").load("file:///home/anand/UvA/ING/Mechanical Turk/5/CPU50.csv")
    df.show()
  }

}
