import pandas as pd
import random
import sqlite3


def generate_people_table(db_path="people.db", num_people=30):
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fay", "George", "Hannah", "Isaac", "Julia"]
    last_names = ["Smith", "Jones", "Taylor", "Brown", "White"]
    genders = ["M", "F"]

    people = []

    for person_id in range(1, num_people + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice(genders)
        father_id = None
        mother_id = None
        spouse_id = None

        if person_id > 6:
            father_id = random.randint(1, person_id - 1)
            mother_id = random.randint(1, person_id - 1)
            if father_id == mother_id:
                mother_id = None

        if person_id % 2 == 0 and person_id < num_people:
            spouse_id = person_id + 1

        people.append((person_id, first_name, last_name, gender, father_id, mother_id, spouse_id))

    # Connect to SQLite and create table
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS people (
            Person_Id INTEGER PRIMARY KEY,
            Personal_Name TEXT,
            Family_Name TEXT,
            Gender TEXT,
            Father_Id INTEGER,
            Mother_Id INTEGER,
            Spouse_Id INTEGER
        )
    """)

    c.execute("DELETE FROM people")  # Clear existing data if any
    c.executemany("""
        INSERT INTO people (Person_Id, Personal_Name, Family_Name, Gender, Father_Id, Mother_Id, Spouse_Id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, people)

    conn.commit()
    conn.close()

    print(f"Created 'people' table with {num_people} entries in {db_path}")
