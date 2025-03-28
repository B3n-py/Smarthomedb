from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",         
        user="root",   
        password="password", 
        database="smarthomedb"    
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM devices LIMIT 5;")
    devices = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", devices=devices)

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users LIMIT 5;")
    users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route('/alerts')
def alerts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alerts LIMIT 10;")
    alerts = cursor.fetchall()
    conn.close()
    return render_template("alerts.html", alerts=alerts)

@app.route('/devices')
def devices():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices;")
    devices = cursor.fetchall()
    conn.close()
    return render_template("devices.html", devices=devices)

@app.route('/devicelogs')
def devicelogs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devicelogs ORDER BY logTime DESC;")
    logs = cursor.fetchall()
    conn.close()
    return render_template("devicelogs.html", logs=logs)

@app.route('/devicepurchase')
def devicepurchase():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT dp.purchaseId, d.deviceName, u.name AS userName, dp.purchaseDate
        FROM devicepurchase dp
        JOIN devices d ON dp.deviceId = d.deviceId
        JOIN users u ON dp.userId = u.userId
        ORDER BY dp.purchaseDate DESC;
    """)
    purchases = cursor.fetchall()
    conn.close()
    return render_template("devicepurchase.html", purchases=purchases)

@app.route('/devicesettings')
def devicesettings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ds.settingId, d.deviceName, ds.settingName, ds.settingValue
        FROM devicesettings ds
        JOIN devices d ON ds.deviceId = d.deviceId
        ORDER BY ds.settingId ASC;
    """)
    settings = cursor.fetchall()
    conn.close()
    return render_template("devicesettings.html", settings=settings)

@app.route('/energyusage')
def energyusage():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT eu.usageId, d.deviceName, eu.usageInKWh, eu.recordedDate
        FROM energyusage eu
        JOIN devices d ON eu.deviceId = d.deviceId
        ORDER BY eu.recordedDate DESC;
    """)
    usage = cursor.fetchall()
    conn.close()
    return render_template("energyusage.html", usage=usage)

@app.route('/maintenance')
def maintenance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.maintenanceId, d.deviceName, m.scheduleDate, m.description
        FROM maintenance m
        JOIN devices d ON m.deviceId = d.deviceId
        ORDER BY m.scheduleDate ASC;
    """)
    maintenance = cursor.fetchall()
    conn.close()
    return render_template("maintenance.html", maintenance=maintenance)

@app.route('/manufacturers')
def manufacturers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM manufacturers ORDER BY name ASC;")
    manufacturers = cursor.fetchall()
    conn.close()
    return render_template("manufacturers.html", manufacturers=manufacturers)

@app.route('/rooms')
def rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms ORDER BY floor, roomName;")
    rooms = cursor.fetchall()
    conn.close()
    return render_template("rooms.html", rooms=rooms)

@app.route('/schedules')
def schedules():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.scheduleId, d.deviceName, s.startTime, s.endTime
        FROM schedules s
        JOIN devices d ON s.deviceId = d.deviceId
        ORDER BY s.startTime;
    """)
    schedules = cursor.fetchall()
    conn.close()
    return render_template("schedules.html", schedules=schedules)


if __name__ == '__main__':
    app.run(debug=True)
