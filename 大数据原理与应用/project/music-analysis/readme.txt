1、软件版本号
Linux: Ubuntu16.04 
Hadoop: 3.1.3
Spark: 2.4.0
Web框架：flask 1.0.3
可视化工具：Echarts
开发工具：Visual Studio Code


2、环境搭建
1) 依照厦大数据库实验室博客上的教程，安装Hadoop3.1.3和Spark2.4.0。
2) 安装Web框架flask
A. 在Ubuntu终端窗口中，用 hadoop 用户登录，在命令行运行su hadoop，并输入用户密码。
B. 进入代码所在目录。
C. 安装pip3，在命令行运行sudo apt-get install python3-pip。
D. 安装flask，运行命令pip3 install flask。


3、程序运行

（1）将数据集存放在分布式文件系统HDFS中
A. 启动Hadoop中的HDFS组件，在命令行运行下面命令：
/usr/local/hadoop/sbin/start-dfs.sh
B. 在hadoop上登录用户创建目录，在命令行运行下面命令：
hdfs dfs –mkdir –p /user/hadoop
C. 把本地文件系统中的数据集albums.csv上传到分布式文件系统HDFS中： 
hdfs dfs –put albums.csv

（2）导出分析数据
A. 在Ubuntu终端窗口中，用 hadoop 用户登录，在命令行运行su hadoop，并输入用户密码。
B. 进入代码所在目录。
C. 为了能够读取HDFS中的albums.csv文件，在命令行运行：
/usr/local/hadoop/sbin/start-dfs.sh
D. 在命令行运行：spark-submit main.py

（3）生成可视化结果
A. 在另一个Ubuntu终端窗口中，用 hadoop 用户登录，在命令行运行su hadoop，并输入用户密码。
B. 进入代码所在目录。
C. 在命令行运行spark-submit SparkFlask.py。
D. 在浏览器打开http://127.0.0.1:5000/

