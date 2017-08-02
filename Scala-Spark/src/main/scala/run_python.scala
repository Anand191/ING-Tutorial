import sys.process._

object run_python {
  def main(args: Array[String]): Unit = {
    val result = "$WORKSPACE/Scala-Spark/JenkinsCI/bin/bokeh serve --show --port 5001 $WORKSPACE/Scala-Spark/Fifth_Trial.py".!
    println(result)
  }

}
