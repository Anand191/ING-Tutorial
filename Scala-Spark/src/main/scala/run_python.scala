import sys.process._

object run_python {
  def main(args: Array[String]): Unit = {
    val result = "JenkinsCI/bin/bokeh serve --show --port 5001 Fifth_Trial.py".!
    println(result)
  }

}
