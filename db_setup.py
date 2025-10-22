import psycopg2

db_config = {
    "dbname": "kafka",
    "user": "maddy",
    "password": "maddy",
    "host": "localhost",
    "port": "5432"
}

def create_orders_table():
    """ Connects to the database and creates the orders table if it doesn't exist. """
    
    create_table_command = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id UUID PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        item VARCHAR(255) NOT NULL,
        quantity INTEGER,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    db_conn = None
    try:
        db_conn = psycopg2.connect(**db_config)
        print("🐘 Successfully connected to PostgreSQL")
        
        with db_conn.cursor() as cursor:
            cursor.execute(create_table_command)
            db_conn.commit()
            print("✅ 'orders' table is ready.")

    except psycopg2.Error as e:
        print(f"🔥 Database Error: {e}")

    finally:
        if db_conn:
            db_conn.close()
            print("🐘 PostgreSQL connection closed")

if __name__ == "__main__":
    create_orders_table()