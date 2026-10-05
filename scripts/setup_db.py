from app.db import get_connection


def run_sql_file(path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Done:", path)


if __name__ == "__main__":
    # WARNING: wipes the database and reloads clean seed data
    run_sql_file("scripts/schema.sql")
    run_sql_file("scripts/seed.sql")