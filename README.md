# bigdata-project-2024 – Pipeline Kafka → HDFS + Analyse MapReduce - Matéo DOMINGUEZ Hugo SCATENA
This **README** describes step by step what we achieved for:

1. Produce logs with a Python script and send them to Kafka.  
2. Consume these logs from Kafka and store them in HDFS. 
3. Analyze the data stored in HDFS via a MapReduce job (in Python with Hadoop Streaming).

---

## 1. Presentation of the project

1. **Log generation in Python** :  
   - A script (`log_generator.py`) continuously generates logs (level, timestamp, etc.) and publishes them in a **Kafka topic** called `logs_machine`

2. **Consumtion Kafka → HDFS** :  
   - Another Python script (`consumer_kafka_to_hdfs.py`) continuously reads messages from the Kafka topic `logs_machine` and, in batches, sends them to **HDFS** (file `logs_machine.txt` in `/user/kafka/ logs/`).

3. **Analyse via MapReduce** :  
   - We wrote a single Python script (`log_mapreduce.py`) which contains both the **mapper** and the **reducer**.  
   - This script is run with **Hadoop Streaming** to count, for example, the number of occurrences of `INFO`, `WARN`, `ERROR`.

The whole constitutes a complete pipeline for managing and analyzing logs:  
1. **Kafka** receives the logs  
2. Logs are stored in **HDFS**  
3. A **MapReduce** job (in Python) does the aggregation/analysis.

---

## 2. Modules / Versions used

- **Operating system**: Windows 10/11  
- **Java**: JDK 17  
- **Python**: 3.11  
- **Kafka**: 3.x (e.g. `kafka_2.12-3.9.0`)  
- **Hadoop**: 3.3.6 (installed in `C:\hadoop\hadoop-3.3.6`)  
  - HDFS enabled in pseudo-distributed mode  
  - Hadoop Streaming binary: `C:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar`  
- **kafka-python**: Python library to produce/consume in Kafka  
- **Hadoop Streaming**: allows you to write the mapper/reducer in Python.

---

## 3. Commands step by step

### 3.1 Kafka : start and configuration

1. **Starting ZooKeeper et Kafka** (en two seperated commands) :  
   ```powershell
   # Terminal 1 - ZooKeeper
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
![image](https://github.com/user-attachments/assets/d14837e0-262c-4321-a176-25a14e3eaebe)

   # Terminal 2 - Kafka Broker
   .\bin\windows\kafka-server-start.bat .\config\server.properties
![image](https://github.com/user-attachments/assets/25d5c5cd-91a8-46a9-bbfd-cf44f01c5387)


   
2. **Create the Kafka logs_machine topic (from a 3rd terminal): **
   ```powershell
   # Terminal 1 - ZooKeeper
   .\bin\windows\kafka-topics.bat --create --topic logs_machine --bootstrap-server localhost:9092 --partitions 3 -- 
   replication-factor 1
   
### 3.2 3.2 Log generation (Python → Kafka)
   - **Script** log_generator.py :
      ```powershell
      .\python log_generator.py
   **It produces continuous logs randomly on the logs_machine topic of 4 different types: [ERROR],[INFO],[WARN] et [DEBUG]**
   
![image](https://github.com/user-attachments/assets/77b7b319-029c-481e-93c5-46fcf5261dad)
![image](https://github.com/user-attachments/assets/83e49396-d203-4f52-ba43-091d6c2dc910)



### 3.3 Verification of arrival and reception of logs (Python → Kafka)
- **Script** consumer.py :
      ```powershell
      .\python consumer.py
  ![image](https://github.com/user-attachments/assets/9427350e-9155-4a18-aa87-012c03b88773)

   
### 3.4 Kafka consumption to HDFS (consumer_kafka_to_hdfs.py)
   1. **start HDFS** (après avoir fait un hdfs namenode -format si besoin) :
       ```powershell
      cd C:\hadoop\hadoop-3.3.6
      .\sbin\start-dfs.cmd
   let the windows NameNode/DataNode open
   .
   2. **Create target folder in HDFS**
       ```powershell
       hdfs dfs -mkdir -p /user/kafka/logs
       hdfs dfs -ls /user/kafka
       
   ![image](https://github.com/user-attachments/assets/4f8ad74a-6ffa-4153-b792-269e8e1f91db)

   3. **Run the Python consumer**
       ```powershell
      cd C:\kafka\my_consumer
      python consumer_kafka_to_hdfs.py
   **Every 60 s it sends the contents of temp_logs.txt** to /user/kafka/logs/logs_machine.txt (en HDFS).

### 3.5 Analyse MapReduce (script unique Python)

   1. **Script  log_mapreduce.py** (after making an hdfs namenode -format if necessary) :
      -Contains run_mapper() and run_reducer() in the same file.
      -Called in “mapper” or “reducer” mode depending on the argument
     
      
   2. **launch the job Hadoop Streaming**
       ```powershell
       hadoop jar "C:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" `
       -files "log_mapreduce.py" `
       -mapper "python log_mapreduce.py mapper" `
       -reducer "python log_mapreduce.py reducer" `
       -input "/user/kafka/logs/*.txt" `
       -output "/user/kafka/logs_out"
       -files log_mapreduce.py: transfers the Python script to the cluster.
       -mapper: executes log_mapreduce.py mapper for the Map phase.
       -reducer: Runs log_mapreduce.py reducer for the Reduce phase.
 ![image](https://github.com/user-attachments/assets/b1aa206a-923c-4f26-9d79-e910c091fc7c)
       
   3. *Verify the result :**
       ```powershell
      hdfs dfs -ls /user/kafka/logs_out
      hdfs dfs -cat /user/kafka/logs_out/part-00000
   **For example, we find the total number of INFO, WARN, ERROR, etc.**
   ![image](https://github.com/user-attachments/assets/9b2bfc8b-d9d7-4afd-acf4-bd1ff22b0082)
   ![image](https://github.com/user-attachments/assets/460f1a28-fac4-499c-bf89-bc4902a86e92)



### 4. Conclusion

   **We have set up :**

   -A pipeline where a Python script generates logs to Kafka.
   -A Python consumer that reads from Kafka and sends logs to HDFS.
   -A MapReduce job in a single Python file (via Hadoop Streaming) to analyze/aggregate data stored in HDFS.

**This pipeline demonstrates complete flow :**
**Production** (Kafka) **→ Storage** (HDFS) **→ Analysis** (MapReduce Python).
   



   
