import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create slots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY,
            available_slots TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO slots (id, available_slots)
        VALUES (1, '100')
    ''')

    # Create pricing table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing (
            plan TEXT PRIMARY KEY,
            price REAL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO pricing (plan, price)
        VALUES ('1 Month', 9.99), ('3 Months', 24.99), ('Lifetime', 99.99)
    ''')

    # Create offerings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offerings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            image TEXT,
            title TEXT,
            description TEXT
        )
    ''')

    # Create live_stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_stats (
            id INTEGER PRIMARY KEY,
            xp_gained INTEGER,
            hours_botted INTEGER,
            unique_builds INTEGER
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO live_stats (id, xp_gained, hours_botted, unique_builds)
        VALUES (1, 0, 0, 0)
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
