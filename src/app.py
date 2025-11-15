import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1) Connect to the database with SQLAlchemy
db_url = os.getenv("DATABASE_URL", "sqlite:///example.db")

engine = create_engine(db_url)

# 2) Create the tables

def create_tables():
    create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            department VARCHAR(100),
            salary NUMERIC
        );
    """)
    # Usamos una transacción para asegurarnos de que se guarde
    with engine.begin() as conn:
        conn.execute(create_table_sql)
    print("Tablas creadas (o ya existían).")
# 3) Insert data

def insert_data():
    # Datos de ejemplo
    employees_data = [
        ("Adrian", "Data Analytics", 2500),
        ("Andrea", "Marketing", 2300),
        ("Miguel", "IT", 2700),
        ("Laura", "HR", 2200),
    ]

    insert_sql = text("""
        INSERT INTO employees (name, department, salary)
        VALUES (:name, :department, :salary);
    """)

    with engine.begin() as conn:
        for name, department, salary in employees_data:
            conn.execute(
                insert_sql,
                {"name": name, "department": department, "salary": salary}
            )
    print("Datos insertados en la tabla employees.")


# 4) Use Pandas to read and display a table

def show_table():
    query = "SELECT * FROM employees;"
    df = pd.read_sql(query, engine)
    print("Datos leídos con Pandas:\n")
    print(df)

if __name__ == "__main__":
    print("Conectando a la base de datos:", db_url)
    create_tables()
    insert_data()
    show_table()

    print("El script está corriendo correctamente")