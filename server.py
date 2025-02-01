from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

API_KEY = os.getenv('API_KEY', 'default_api_key')  # Use environment variable for API key
app.logger.debug(f'Loaded API_KEY: {API_KEY}')  # Debug statement to verify API key

def get_available_slots():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT available_slots FROM slots WHERE id = 1')
    available_slots = cursor.fetchone()[0]
    conn.close()
    return available_slots

def update_available_slots(new_slots):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE slots SET available_slots = ? WHERE id = 1', (str(new_slots),))
    conn.commit()
    conn.close()

def get_pricing():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT plan, price FROM pricing')
    pricing = cursor.fetchall()
    app.logger.debug(f'Fetched pricing: {pricing}')
    conn.close()
    return pricing

def update_pricing(plan, price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    app.logger.debug(f'Updating pricing for {plan} to {price}')
    cursor.execute('UPDATE pricing SET price = ? WHERE plan = ?', (price, plan))
    conn.commit()
    conn.close()

def init_offerings_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offerings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            image TEXT,
            title TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_offering_to_db(tag, image, title, description):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO offerings (tag, image, title, description)
        VALUES (?, ?, ?, ?)
    ''', (tag, image, title, description))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def remove_offering_from_db(offering_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM offerings WHERE id = ?', (offering_id,))
    conn.commit()
    conn.close()

def edit_offering_in_db(offering_id, tag, image, title, description):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE offerings
        SET tag = ?, image = ?, title = ?, description = ?
        WHERE id = ?
    ''', (tag, image, title, description, offering_id))
    conn.commit()
    conn.close()

def get_all_offerings():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, tag, image, title, description FROM offerings")
    offerings = cursor.fetchall()
    conn.close()
    return offerings

def init_live_stats_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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

def get_live_stats():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT xp_gained, hours_botted, unique_builds FROM live_stats WHERE id = 1')
    live_stats = cursor.fetchone()
    conn.close()
    return live_stats

def update_live_stats(xp_gained=None, hours_botted=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if xp_gained is not None:
        cursor.execute('UPDATE live_stats SET xp_gained = ? WHERE id = 1', (xp_gained,))
    if hours_botted is not None:
        cursor.execute('UPDATE live_stats SET hours_botted = ? WHERE id = 1', (hours_botted,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    try:
        available_slots = get_available_slots()
        pricing = get_pricing()
        offerings = get_all_offerings()
        live_stats = get_live_stats()
        return render_template('home.html',
                               available_slots=available_slots,
                               pricing=pricing,
                               offerings=offerings,
                               xp_gained=live_stats[0],
                               hours_botted=live_stats[1],
                               unique_builds=live_stats[2])
    except Exception as e:
        app.logger.error(f"Error in home route: {e}")
        return "Internal Server Error", 500

@app.route('/update_slots', methods=['POST'])
def update_slots():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403

        app.logger.debug(f'Received data: {data}')
        new_slots = data.get('available_slots')
        if new_slots is not None:
            # If new_slots is not an integer, set it to "maintenance"
            if not str(new_slots).isdigit():
                new_slots = 'maintenance'
            update_available_slots(new_slots)
            app.logger.debug(f'Successfully updated slots to {new_slots}')
            return jsonify({'status': 'success', 'available_slots': new_slots}), 200
        else:
            app.logger.error('Invalid data received')
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        app.logger.error(f"Error in update_slots endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/update_pricing', methods=['POST'])
def update_pricing_endpoint():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403

        app.logger.debug(f'Received data: {data}')
        plan = data.get('plan')
        price = data.get('price')
        if plan and price is not None:
            update_pricing(plan, price)
            app.logger.debug(f'Successfully updated pricing for {plan} to {price}')
            return jsonify({'status': 'success', 'plan': plan, 'price': price}), 200
        else:
            app.logger.error('Invalid data received')
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        app.logger.error(f"Error in update_pricing endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/add_offering', methods=['POST'])
def add_offering():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key on add_offering')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403
        tag = data.get('tag')
        image = data.get('image')
        title = data.get('title')
        description = data.get('description')
        if not all([tag, image, title, description]):
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        new_id = add_offering_to_db(tag, image, title, description)
        return jsonify({'status': 'success', 'id': new_id}), 200
    except Exception as e:
        app.logger.error(f"Error in add_offering endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/remove_offering', methods=['POST'])
def remove_offering():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key on remove_offering')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403
        offering_id = data.get('id')
        if offering_id is None:
            return jsonify({'status': 'error', 'message': 'Missing offering id'}), 400
        remove_offering_from_db(offering_id)
        return jsonify({'status': 'success', 'removed_id': offering_id}), 200
    except Exception as e:
        app.logger.error(f"Error in remove_offering endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/edit_offering', methods=['POST'])
def edit_offering():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key on edit_offering')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403
        offering_id = data.get('id')
        tag = data.get('tag')
        image = data.get('image')
        title = data.get('title')
        description = data.get('description')
        if not offering_id or not all([tag, image, title, description]):
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        edit_offering_in_db(offering_id, tag, image, title, description)
        return jsonify({'status': 'success', 'edited_id': offering_id}), 200
    except Exception as e:
        app.logger.error(f"Error in edit_offering endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/offerings', methods=['GET'])
def get_offerings():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, tag, image, title, description FROM offerings")
        offerings = cursor.fetchall()
        return jsonify({'offerings': offerings})
    except Exception as e:
        app.logger.error(f"Error fetching offerings: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/update_xp_gained', methods=['POST'])
def update_xp_gained():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403

        xp_gained = data.get('xp_gained')
        if xp_gained is not None:
            update_live_stats(xp_gained=xp_gained)
            app.logger.debug(f'Successfully updated XP gained to {xp_gained}')
            return jsonify({'status': 'success', 'xp_gained': xp_gained}), 200
        else:
            app.logger.error('Invalid data received')
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        app.logger.error(f"Error in update_xp_gained endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/update_hours_botted', methods=['POST'])
def update_hours_botted():
    try:
        data = request.get_json()
        api_key = request.headers.get('API-Key')
        app.logger.debug(f'Received API key: {api_key}')  # Debug statement to log received API key
        app.logger.debug(f'Expected API key: {API_KEY}')  # Debug statement to log expected API key
        if api_key != API_KEY:
            app.logger.error('Invalid API key')
            return jsonify({'status': 'error', 'message': 'Invalid API key'}), 403

        hours_botted = data.get('hours_botted')
        if hours_botted is not None:
            update_live_stats(hours_botted=hours_botted)
            app.logger.debug(f'Successfully updated hours botted to {hours_botted}')
            return jsonify({'status': 'success', 'hours_botted': hours_botted}), 200
        else:
            app.logger.error('Invalid data received')
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        app.logger.error(f"Error in update_hours_botted endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/api/live_stats', methods=['GET'])
def api_live_stats():
    try:
        live_stats = get_live_stats()
        return jsonify({
            'xp_gained': live_stats[0],
            'hours_botted': live_stats[1],
            'unique_builds': live_stats[2]
        }), 200
    except Exception as e:
        app.logger.error(f"Error in api_live_stats endpoint: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    init_live_stats_table()
    app.run(host='0.0.0.0', port=8095)
