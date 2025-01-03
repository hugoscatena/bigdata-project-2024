# bigdata-project-2024 – Pipeline Kafka → HDFS + Analyse MapReduce - Matéo DOMINGUEZ Hugo SCATENA
Ce **README** décrit pas à pas ce que nous avons réalisé pour :

1. Produire des logs avec un script Python et les envoyer dans Kafka.  
2. Consommer ces logs depuis Kafka et les stocker dans HDFS.  
3. Analyser les données stockées dans HDFS via un job MapReduce (en Python avec Hadoop Streaming).

---

## 1. Présentation du projet

1. **Génération de logs en Python** :  
   - Un script (`log_generator.py`) génère en continu des logs (niveau, timestamp, etc.) et les publie dans un **topic Kafka** appelé `logs_machine`.

2. **Consommation Kafka → HDFS** :  
   - Un autre script Python (`consumer_kafka_to_hdfs.py`) lit en continu les messages du topic Kafka `logs_machine` et, par lots, les envoie vers **HDFS** (fichier `logs_machine.txt` dans `/user/kafka/logs/`).

3. **Analyse via MapReduce** :  
   - Nous avons écrit un script unique Python (`log_mapreduce.py`) qui contient à la fois le **mapper** et le **reducer**.  
   - Ce script est exécuté avec **Hadoop Streaming** pour compter, par exemple, le nombre d’occurrences de `INFO`, `WARN`, `ERROR`.

L’ensemble constitue un pipeline complet pour gérer et analyser des logs :  
1. **Kafka** reçoit les logs  
2. Les logs sont stockés dans **HDFS**  
3. Un job **MapReduce** (en Python) fait l’agrégation/analyse.

---

## 2. Modules / Versions utilisées

- **Système d’exploitation** : Windows 10/11  
- **Java** : JDK 17  
- **Python** : 3.11  
- **Kafka** : 3.x (ex. `kafka_2.12-3.9.0`)  
- **Hadoop** : 3.3.6 (installé dans `C:\hadoop\hadoop-3.3.6`)  
  - HDFS activé en mode pseudo-distribué  
  - Binaire de Hadoop Streaming : `C:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar`  
- **kafka-python** : bibliothèque Python pour produire/consommer dans Kafka  
- **Hadoop Streaming** : permet d’écrire le mapper/reducer en Python.

---

## 3. Commandes à chaque étape

### 3.1 Kafka : démarrage et configuration

1. **Démarrer ZooKeeper et Kafka** (en deux terminaux séparés) :  
   ```powershell
   # Terminal 1 - ZooKeeper
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

   # Terminal 2 - Kafka Broker
   .\bin\windows\kafka-server-start.bat .\config\server.properties

   
2. **Créer le topic Kafka logs_machine (depuis un 3ᵉ terminal) : 
   ```powershell
   # Terminal 1 - ZooKeeper
   .\bin\windows\kafka-topics.bat --create --topic logs_machine --bootstrap-server localhost:9092 --partitions 3 -- 
   replication-factor 1
   
### 3.2 Génération de logs (Python → Kafka)


   
