import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("hr.db")
c = conn.cursor()

for i in range(100):   # 👈 هنا العدد
    c.execute(
        """
        INSERT INTO employees (name, department, position, salary)
        VALUES (?, ?, ?, ?)
        """,
        (
            fake.name(),
            fake.company(),
            fake.job(),
            float(random.randint(3000, 15000))
        )
    )

conn.commit()
conn.close()

print("100 employees inserted ")