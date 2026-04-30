import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="skillpath_db",
    user="postgres",
    password="123456789"
)

def get_cursor():
    return conn.cursor()
def get_skills_by_domain(domain):
    cursor = get_cursor()

    cursor.execute("""
        SELECT s.name
        FROM skills s
        JOIN domains1 d ON s.domain_id = d.id
        WHERE LOWER(d.name) LIKE %s
    """, (domain.lower() + "%",))

    skills = [row[0] for row in cursor.fetchall()]

    print("DB SKILLS:", skills)  # debug

    return skills
