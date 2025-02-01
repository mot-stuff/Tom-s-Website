import sqlite3
# ==================================================================================================
# DO NOT RUN THIS FILE UNLESS YOU WANT TO RESET THE DATABASE/CORRUPT THE DATABASE
# ONLY RUN THIS FILE IF YOU WANT TO RESET THE DATABASE TO ITS INITIAL STATE WITH BASE OFFERINGS
# It is crucial database.db is not deleted or corrupted as it contains all the data for the website's cards.
# ==================================================================================================
def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS slots')
    cursor.execute('DROP TABLE IF EXISTS pricing')
    cursor.execute('DROP TABLE IF EXISTS offerings')
    cursor.execute('DROP TABLE IF EXISTS live_stats')
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY,
            available_slots TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR REPLACE INTO slots (id, available_slots)
        VALUES (1, '100')
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing (
            plan TEXT PRIMARY KEY,
            price REAL
        )
    ''')
    cursor.executemany('''
        INSERT OR REPLACE INTO pricing (plan, price)
        VALUES (?, ?)
    ''', [('1 Month', 9.99), ('3 Months', 24.99), ('Lifetime', 99.99)])
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offerings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            image TEXT,
            title TEXT,
            description TEXT
        )
    ''')
    initial_offerings = [
        ("Skilling", "/images/woodcutting.png", "Woodcutter", "w/ banking/power/wc guild planks"),
        ("Skilling", "/images/agility.png", "Rooftop Agility", "Agility training on rooftops"),
        ("Skilling", "/images/fletching.png", "Fletching", "Craft bows and arrows"),
        # Add more offerings as needed
    ]
    cursor.executemany('''
        INSERT INTO offerings (tag, image, title, description)
        VALUES (?, ?, ?, ?)
    ''', initial_offerings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_stats (
            id INTEGER PRIMARY KEY,
            xp_gained INTEGER,
            hours_botted INTEGER,
            unique_builds INTEGER
        )
    ''')
    cursor.execute('''
        INSERT OR REPLACE INTO live_stats (id, xp_gained, hours_botted, unique_builds)
        VALUES (1, 0, 0, 0)
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup successfully.")
