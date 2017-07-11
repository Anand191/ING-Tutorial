/**
  * Created by anand on 7/11/17.
  */
import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}
object test_object {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("Datasets Test")
    conf.setMaster("local[*]")
    val sc = new SparkContext(conf)
    println(sc)

    val NUM_SAMPLES = 150000
    val count = sc.parallelize(1 to NUM_SAMPLES).filter { _ =>
      val x = math.random
      val y = math.random
      x*x + y*y < 1
    }.count()
    println(s"Pi is roughly ${4.0 * count / NUM_SAMPLES}")


    val textFile = sc.textFile("README.md")
    val counts = textFile.flatMap(line => line.split(" "))
      .map(word => (word, 1))
      .reduceByKey(_ + _)
    counts.foreach(println)
  }
}