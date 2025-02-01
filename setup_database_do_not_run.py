import sqlite3
# ==================================================================================================
# DO NOT RUN THIS FILE UNLESS YOU WANT TO RESET THE DATABASE/CORRUPT THE DATABASE
# ONLY RUN THIS FILE IF YOU WANT TO RESET THE DATABASE TO ITS INITIAL STATE WITH 3 BASE OFFERINGS
# ==================================================================================================
def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS slots')
    cursor.execute('DROP TABLE IF EXISTS pricing')
    cursor.execute('DROP TABLE IF EXISTS offerings')
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY,
            available_slots TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR REPLACE INTO slots (id, available_slots)
        VALUES (1, '40')
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing (
            plan TEXT PRIMARY KEY,
            price INTEGER
        )
    ''')
    cursor.executemany('''
        INSERT OR REPLACE INTO pricing (plan, price)
        VALUES (?, ?)
    ''', [('1 Month', 15), ('3 Months', 40), ('Lifetime', 500)])
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
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
