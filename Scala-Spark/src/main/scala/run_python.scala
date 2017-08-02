import sys.process._
object run_python {
  def main(args: Array[String]): Unit = {
    val result = "/var/lib/jenkins/workspace/ING_Turk/Scala-Spark/JenkinsCI/bin/bokeh serve --show --port 5001 /var/lib/jenkins/workspace/ING_Turk/Scala-Spark/Fifth_Trial.py".!
    println(result)
  }

}
