# Solution for chapter 10

## using spark shell for coding

### start Spark shell

```shell

Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.0
      /_/

Using Scala version 2.11.12 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_202)
Type in expressions to have them evaluated.
Type :help for more information.
```

### Read file

#### Read local file

```scala
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.0
      /_/

Using Scala version 2.11.12 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_202)
Type in expressions to have them evaluated.
Type :help for more information.

scala> val textFile = sc.textFile("file:///usr/local/spark/README.md")
textFile: org.apache.spark.rdd.RDD[String] = file:///usr/local/spark/README.md MapPartitionsRDD[1] at textFile at <console>:24

scala> textFile.first()
res0: String = # Apache Spark
```

#### Read HDFS file

```shell
scala> val textFile = sc.textFile("hdfs://localhost:9000/README.md")
textFile: org.apache.spark.rdd.RDD[String] = hdfs://localhost:9000/README.md MapPartitionsRDD[3] at textFile at <console>:24

scala> textFile.first()
res1: String = # Apache Spark

scala> val wordCount = textFile.flatMap(line=>line.split(" ")).map(word => (word, 1)).reduceByKey((a,b)=>a+b)
wordCount: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[6] at reduceByKey at <console>:25

scala> wordCount.collect()
res2: Array[(String, Int)] = Array((package,1), (this,1), (integration,1), (Python,2), (page](http://spark.apache.org/documentation.html).,1), (cluster.,1), (its,1), ([run,1), (There,1), (general,3), (have,1), (pre-built,1), (Because,1), (YARN,,1), (locally,2), (changed,1), (locally.,1), (sc.parallelize(1,1), (only,1), (several,1), (This,2), (basic,1), (Configuration,1), (learning,,1), (documentation,3), (first,1), (graph,1), (Hive,2), (info,1), (["Specifying,1), ("yarn",1), ([params]`.,1), ([project,1), (prefer,1), (SparkPi,2), (<http://spark.apache.org/>,1), (engine,1), (version,1), (file,1), (documentation,,1), (MASTER,1), (example,3), (["Parallel,1), (are,1), (params,1), (scala>,1), (DataFrames,,1), (provides,1), (refer,2), (configure,1), (Interactive,2), (R,,1), (can,7), (build,4),...
scala>
```

### Spark 独立应用程序

#### scala语言

#### 安装sbt

```shell
hadoop@Hale:/usr/local/sbt$ ./sbt sbtVersion
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=256M; support was removed in 8.0
[warn] No sbt.version set in project/build.properties, base directory: /usr/local/sbt
[info] Set current project to sbt (in build file:/usr/local/sbt/)
[info] 1.3.8
```

#### 编写具体的scala程序

使用原生的`vim`完成代码的编写和准备得到

```shell
$ find .
.
./src
./src/main
./src/main/scala
./src/main/scala/SimpleApp.scala
./simple.sbt
```

使用命令`/usr/local/sbt/sbt package`完成对源文件的打包得到如下的输出:

```shell
[info] Fetched artifacts of
[warn] There may be incompatibilities among your library dependencies; run 'evicted' to see detailed eviction warnings.
[info] Compiling 1 Scala source to /home/hadoop/sparkapp/target/scala-2.11/classes ...
https://repo1.maven.org/maven2/org/scala-sbt/compiler-bridge_2.11/1.3.4/compiler-bridge_2.11-1.3.4.pom
  100.0% [##########] 2.8 KiB (12.9 KiB / s)
https://repo1.maven.org/maven2/org/scala-sbt/util-interface/1.3.0/util-interface-1.3.0.jar
  100.0% [##########] 2.5 KiB (12.6 KiB / s)
[info] Non-compiled module 'compiler-bridge_2.11' for Scala 2.11.12. Compiling...
[info]   Compilation completed in 7.344s.
[success] Total time: 61 s (01:01), completed Jun 5, 2024 11:34:50 PM
```

可以观察到产生了新的`jar`包

```shell
hadoop@Hale:~/sparkapp$ find . | grep '.*2.11-1.0.jar'
./target/scala-2.11/simple-project_2.11-1.0.jar
```

提交到`sbt`进行执行即可

```shell
hadoop@Hale:~/sparkapp$ /usr/local/spark/bin/spark-submit --class "SimpleApp" ~/sparkapp/target/scala-2.11/simple-project_2.11-1.0.jar 2>&1 | grep "Lines with a:"
Lines with a: 62, Lines with b: 31
```

#### java 语言

#### 安装maven

```shell
hadoop@Hale:/usr/local/maven/bin$ ./mvn -version
Apache Maven 3.9.7 (8b094c9513efc1b9ce2d952b3b9c8eaedaf8cbf0)
Maven home: /usr/local/maven
Java version: 1.8.0_202, vendor: Oracle Corporation, runtime: /usr/lib/jvm/jdk1.8.0_202/jre
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "5.15.146.1-microsoft-standard-wsl2", arch: "amd64", family: "unix"
```

#### 编写具体的java程序

```shell
hadoop@Hale:~/sparkapp2$ find .
.
./src
./src/main
./src/main/java
./src/main/java/SimpleApp.java
./pom.xml
```

打包程序得到如下的输出

```shell
[INFO] Building jar: /home/hadoop/sparkapp2/target/simple-project-1.0.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  48.914 s
[INFO] Finished at: 2024-06-05T23:49:43+08:00
[INFO] ------------------------------------------------------------------------
```

得到结果

```shell
hadoop@Hale:~/sparkapp2$ /usr/local/spark/bin/spark-submit --class "SimpleApp" ./target/simple-project-1.0.jar 2>&1 | grep "Lines"
Lines with a: 62, lines with b: 31
```
