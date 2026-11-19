import sqlite3
import json

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Get tables
cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name LIKE 'club_booking%' ORDER BY name;")
tables = cur.fetchall()

# Table row counts
table_counts = {}
for tbl, sql in tables:
    cur.execute(f"SELECT count(*) FROM {tbl};")
    table_counts[tbl] = cur.fetchone()[0]

# Get bookings
cur.execute("""
SELECT b.id, b.booking_number, c.last_name || ' ' || c.first_name, r.title, b.booking_date, b.time_start, b.time_end, b.players_count, b.total_cost, b.deposit_amount, b.status
FROM club_booking_booking b
JOIN club_booking_client c ON b.client_id = c.id
JOIN club_booking_clubresource r ON b.resource_id = r.id
ORDER BY b.id
LIMIT 25;
""")
booking_rows = cur.fetchall()

data = {
    'tables': tables,
    'table_counts': table_counts,
    'bookings': booking_rows,
    'total_bookings': table_counts.get('club_booking_booking', 0)
}

with open('db_preview_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Export complete. Tables:', len(tables), 'Bookings:', len(booking_rows))
