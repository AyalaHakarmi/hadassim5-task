from generate_people import generate_people_table
from complete_spouses import complete_spouses
from build_family_tree import build_family_tree
import sqlite3
import pandas as pd
import os


def print_table_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    print(f"\nContents of table '{table_name}':")
    print(df.to_string(index=False))


def main():
    db_path = "people.db"

    use_existing = input("Do you have an existing database file with a people table? (y/n): ").strip().lower()
    if use_existing == "y":
        db_path = input("Enter the path to your existing .db file: ").strip()
        if not os.path.exists(db_path):
            print("Error: The specified file does not exist.")
            return
    else:
        print("Generating people table...")
        generate_people_table(db_path=db_path)

    print("Completing spouse connections...")
    complete_spouses(db_path=db_path)

    print("Building family tree...")
    build_family_tree(db_path=db_path)

    view_input = input("\nWould you like to view the input table? (y/n): ").strip().lower()
    if view_input == "y":
        print_table_from_db(db_path, "people")

    view_output = input("\nWould you like to view the output table (family relations)? (y/n): ").strip().lower()
    if view_output == "y":
        print_table_from_db(db_path, "family_relations")

    print("\nAll steps completed. Family tree saved in database.")


if __name__ == "__main__":
    main()
