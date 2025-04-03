import sqlite3

def complete_spouses(db_path="people.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Load all people and their spouse references
    c.execute("SELECT Person_Id, Spouse_Id FROM people")
    people = c.fetchall()

    spouse_map = {person_id: spouse_id for person_id, spouse_id in people if spouse_id is not None}

    updates = []
    for person_id, spouse_id in spouse_map.items():
        # Check if the spouse has a reciprocal reference
        c.execute("SELECT Spouse_Id FROM people WHERE Person_Id = ?", (spouse_id,))
        result = c.fetchone()
        if result:
            their_spouse = result[0]
            if their_spouse is None:
                # No reciprocal reference – update it
                updates.append((person_id, spouse_id))
            elif their_spouse != person_id:
                print(f"Conflict: {person_id} claims {spouse_id} as spouse, but {spouse_id} has {their_spouse} instead.")

    # Apply updates
    for source_id, target_id in updates:
        c.execute("UPDATE people SET Spouse_Id = ? WHERE Person_Id = ?", (source_id, target_id))

    conn.commit()
    conn.close()

    print(f"Spouse completion: {len(updates)} records updated.")
