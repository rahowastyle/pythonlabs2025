import sqlite3
from datetime import datetime, timedelta

DB_NAME = "security_logs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EventSources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        location TEXT,
        type TEXT
    )
    ''')
  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EventTypes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT UNIQUE NOT NULL,
        severity TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SecurityEvents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        source_id INTEGER,
        event_type_id INTEGER,
        message TEXT,
        ip_address TEXT,
        username TEXT,
        FOREIGN KEY (source_id) REFERENCES EventSources (id),
        FOREIGN KEY (event_type_id) REFERENCES EventTypes (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База даних та таблиці ініціалізовано.")

def register_source(name, location, src_type):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)",
                     (name, location, src_type))
        conn.commit()
        print(f"Джерело '{name}' додано.")
    except sqlite3.IntegrityError:
        print(f"Джерело '{name}' вже існує.")
    finally:
        conn.close()

def register_event_type(type_name, severity):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)",
                     (type_name, severity))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # already exists
    finally:
        conn.close()

def log_event(source_name, event_type_name, message, ip_address=None, username=None):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source_name,))
    src_res = cursor.fetchone()

    cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type_name,))
    type_res = cursor.fetchone()

    if src_res and type_res:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, src_res[0], type_res[0], message, ip_address, username))
        conn.commit()
    else:
        print("Помилка: Невідоме джерело або тип події.")
    
    conn.close()
def get_failed_logins_last_24h():
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''
    SELECT se.timestamp, se.username, se.ip_address, es.name
    FROM SecurityEvents se
    JOIN EventTypes et ON se.event_type_id = et.id
    JOIN EventSources es ON se.source_id = es.id
    WHERE et.type_name = 'Login Failed'
      AND se.timestamp >= datetime('now', '-24 hours')
    '''
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n--- Login Failed за останні 24 години ({len(rows)}) ---")
    for row in rows:
        print(f"Time: {row[0]} | User: {row[1]} | IP: {row[2]} | Source: {row[3]}")

def detect_brute_force():
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
    SELECT se.ip_address, COUNT(*) as attempt_count
    FROM SecurityEvents se
    JOIN EventTypes et ON se.event_type_id = et.id
    WHERE et.type_name = 'Login Failed'
      AND se.timestamp >= datetime('now', '-1 hour')
    GROUP BY se.ip_address
    HAVING attempt_count > 5
    '''
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    
    print("\n--- ПОПЕРЕДЖЕННЯ: Підозра на Brute-force (більше 5 спроб/год) ---")
    if not rows:
        print("Підозрілих активностей не виявлено.")
    for row in rows:
        print(f"IP: {row[0]} | Кількість спроб: {row[1]}")

def get_critical_events_last_week():
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
    SELECT es.name, COUNT(*) as count, GROUP_CONCAT(et.type_name)
    FROM SecurityEvents se
    JOIN EventTypes et ON se.event_type_id = et.id
    JOIN EventSources es ON se.source_id = es.id
    WHERE et.severity = 'Critical'
      AND se.timestamp >= datetime('now', '-7 days')
    GROUP BY es.name
    '''
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    
    print("\n--- Критичні події за тиждень (по джерелах) ---")
    for row in rows:
        print(f"Джерело: {row[0]} | Кількість: {row[1]} | Типи: {row[2]}")

def search_keywords(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
    SELECT timestamp, message FROM SecurityEvents
    WHERE message LIKE ?
    '''

    cursor.execute(sql, (f'%{keyword}%',))
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n--- Пошук за словом '{keyword}' ---")
    for row in rows:
        print(f"{row[0]}: {row[1]}")

if __name__ == "__main__":
    init_db()

    event_types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]
    for name, severity in event_types:
        register_event_type(name, severity)
        
    register_source("Firewall_Main", "Server Room", "Firewall")
    register_source("Auth_Server_AD", "Cloud AWS", "Active Directory")
    register_source("Employee_Laptop_1", "Office 204", "Endpoint")

    print("Генерація тестових даних...")
    
    log_event("Auth_Server_AD", "Login Success", "User admin logged in", "192.168.1.10", "admin")
    log_event("Firewall_Main", "Port Scan Detected", "Detected scan on port 22", "45.33.22.11")
    log_event("Employee_Laptop_1", "Malware Alert", "Trojan.Win32 detected", "10.0.0.55", "user1")
    
    # СИМУЛЯЦІЯ АТАКИ (Brute Force)
    attacker_ip = "185.100.100.1"
    for i in range(7):
        log_event("Auth_Server_AD", "Login Failed", f"Invalid password attempt {i+1}", attacker_ip, "root")

    get_failed_logins_last_24h()
    detect_brute_force()
    get_critical_events_last_week()
    search_keywords("Trojan")
