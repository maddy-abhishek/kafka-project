import json
import psycopg2
from confluent_kafka import Consumer

# --- Kafka Consumer Configuration ---
consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-postgres-storage-group",
    "auto.offset.reset": "earliest"
}

# --- PostgreDB Configuration
db_config = {
    "dbname": "kafka",
    "user": "maddy",
    "password": "maddy",
    "host": "localhost",
    "port": "5432"
}

# --- Main Script ---
consumer = Consumer(consumer_config)
consumer.subscribe(["orders"])
print("🟢 Kafka Consumer is running and subscribed to 'orders' topic")

db_conn = None
try:
    db_conn = psycopg2.connect(**db_config)
    print("🐘 Successfully connected to PostgreSQL")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"❌ Kafka Error: {msg.error()}")
            continue

        value = msg.value().decode("utf-8")
        order = json.loads(value)
        print(f"📦 Received order: {order['quantity']} x {order['item']} from {order['user']}")

        try:
            with db_conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO orders (order_id, user_name, item, quantity)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (
                    order['order_id'],
                    order['user'],
                    order['item'],
                    order['quantity']
                ))
                db_conn.commit()
                print(f"✅ Stored order {order['order_id']} in PostgreSQL")

        except Exception as e:
            print(f"🔥 Database Error: {e}")
            if db_conn:
                db_conn.rollback()

except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")
except psycopg2.Error as e:
    print(f"🐘 PostgreSQL connection failed: {e}")
finally:
    if db_conn:
        db_conn.close()
        print("🐘 PostgreSQL connection closed")
    consumer.close()
    print("🟢 Kafka consumer closed")