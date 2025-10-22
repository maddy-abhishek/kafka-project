# Kafka to PostgreSQL Data Pipeline 🚀

This project demonstrates a simple, real-time data pipeline using Apache Kafka and PostgreSQL. A Python producer sends messages to a Kafka topic, and a consumer reads these messages and stores them in a PostgreSQL database. The entire infrastructure is managed with Docker.



---

## ✨ Features

* **Dockerized Kafka**: Runs a single-node Kafka cluster using KRaft mode (no ZooKeeper needed).
* **Python Producer**: Generates sample order data and sends it to a Kafka topic.
* **Python Consumer**: Consumes order data from the Kafka topic and persists it to a PostgreSQL database.
* **Database Setup Script**: Includes a script to automatically create the necessary table in PostgreSQL.

---

## 🛠️ Tech Stack

* **Docker & Docker Compose**: For containerizing and running Kafka.
* **Apache Kafka**: As the message broker for the data stream.
* **PostgreSQL**: As the destination database for storing the data.
* **Python**: For the producer and consumer logic.
    * `confluent-kafka-python`: Kafka client library.
    * `psycopg2-binary`: PostgreSQL adapter for Python.

---

## 📂 Project Structure

```
.
├── docker-compose.yaml     # Defines the Kafka service
├── db_setup.py             # Sets up the PostgreSQL 'orders' table
├── producer.py             # Sends messages to the 'orders' topic
└── consumer.py             # Reads messages and saves them to the database
```

---

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

* **Docker and Docker Compose**: Make sure they are installed and running. [Installation Guide](https://docs.docker.com/get-docker/)
* **Python 3.8+** and `pip`.
* A running **PostgreSQL** instance.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

### 2. Start the Kafka Service

Run the following command in your terminal to start the Kafka container in the background.

```bash
docker-compose up -d
```

### 3. Install Python Dependencies

Install the required Python libraries.

```bash
pip3 install confluent-kafka-python psycopg2-binary
```

### 4. Configure Database Connection

You must update your PostgreSQL connection details in two files:
* `db_setup.py`
* `consumer.py`

Look for the `db_config` dictionary in both files and replace the placeholder values with your actual credentials.

```python
# ⚠️ UPDATE YOUR DATABASE DETAILS HERE
db_config = {
    "dbname": "your_db_name",
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "localhost",
    "port": "5432"
}
```

---

## ▶️ How to Run the Pipeline

Open three separate terminals in the project directory.

### Terminal 1: Set up the Database

Run this script **once** to create the `orders` table in your database.

```bash
python db_setup.py
```

### Terminal 2: Start the Consumer

The consumer will start listening for messages from the Kafka topic.

```bash
python consumer.py
```

### Terminal 3: Run the Producer

Run the producer to send a sample message. You can run this script multiple times to send more messages.

```bash
python producer.py
```

## Validate that the topic was created in kafka container

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

## Describe that topic and see its partitions

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic new_orders
```

## View all events in a topic

```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning
```
