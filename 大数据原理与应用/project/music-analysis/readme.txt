1������汾��
Linux: Ubuntu16.04 
Hadoop: 3.1.3
Spark: 2.4.0
Web��ܣ�flask 1.0.3
���ӻ����ߣ�Echarts
�������ߣ�Visual Studio Code


2�������
1) �����ô����ݿ�ʵ���Ҳ����ϵĽ̳̣���װHadoop3.1.3��Spark2.4.0��
2) ��װWeb���flask
A. ��Ubuntu�ն˴����У��� hadoop �û���¼��������������su hadoop���������û����롣
B. �����������Ŀ¼��
C. ��װpip3��������������sudo apt-get install python3-pip��
D. ��װflask����������pip3 install flask��


3����������

��1�������ݼ�����ڷֲ�ʽ�ļ�ϵͳHDFS��
A. ����Hadoop�е�HDFS������������������������
/usr/local/hadoop/sbin/start-dfs.sh
B. ��hadoop�ϵ�¼�û�����Ŀ¼���������������������
hdfs dfs �Cmkdir �Cp /user/hadoop
C. �ѱ����ļ�ϵͳ�е����ݼ�albums.csv�ϴ����ֲ�ʽ�ļ�ϵͳHDFS�У� 
hdfs dfs �Cput albums.csv

��2��������������
A. ��Ubuntu�ն˴����У��� hadoop �û���¼��������������su hadoop���������û����롣
B. �����������Ŀ¼��
C. Ϊ���ܹ���ȡHDFS�е�albums.csv�ļ��������������У�
/usr/local/hadoop/sbin/start-dfs.sh
D. �����������У�spark-submit main.py

��3�����ɿ��ӻ����
A. ����һ��Ubuntu�ն˴����У��� hadoop �û���¼��������������su hadoop���������û����롣
B. �����������Ŀ¼��
C. ������������spark-submit SparkFlask.py��
D. ���������http://127.0.0.1:5000/

