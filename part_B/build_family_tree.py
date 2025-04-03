import sqlite3

def build_family_tree(db_path="people.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Load all people into memory
    c.execute("SELECT Person_Id, Gender, Father_Id, Mother_Id, Spouse_Id FROM people")
    people = c.fetchall()
    people_by_id = {row[0]: row for row in people}

    relations = set()

    for person in people:
        pid, gender, father_id, mother_id, spouse_id = person

        # Add parent-child relationships
        if father_id:
            relations.add((pid, father_id, "father"))
            relations.add((father_id, pid, "son" if gender == "M" else "daughter"))
        if mother_id:
            relations.add((pid, mother_id, "mother"))
            relations.add((mother_id, pid, "son" if gender == "M" else "daughter"))

        # Add spouse relationship
        if spouse_id:
            relation_type = "wife" if gender == "M" else "husband"
            relations.add((pid, spouse_id, relation_type))

    # Add sibling relationships (shared parents)
    for a in people:
        for b in people:
            if a[0] != b[0] and a[2] == b[2] and a[3] == b[3] and a[2] and a[3]:
                rel_a = "brother" if b[1] == "M" else "sister"
                rel_b = "brother" if a[1] == "M" else "sister"
                relations.add((a[0], b[0], rel_a))
                relations.add((b[0], a[0], rel_b))

    # Create the final family_relations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS family_relations (
            Person_Id INTEGER,
            Relative_Id INTEGER,
            Connection_Type TEXT,
            PRIMARY KEY (Person_Id, Relative_Id)
        )
    """)

    c.execute("DELETE FROM family_relations")
    c.executemany("""
        INSERT OR REPLACE INTO family_relations (Person_Id, Relative_Id, Connection_Type)
        VALUES (?, ?, ?)
    """, list(relations))

    conn.commit()
    conn.close()

    print(f"Family tree built with {len(relations)} relations.")
