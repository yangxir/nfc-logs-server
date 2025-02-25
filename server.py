from flask import Flask, request, render_template
import sqlite3
import datetime
import os

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect("nfc_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            timestamp TEXT,
            ip TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 记录 NFC 访问日志
@app.route("/log_nfc", methods=["POST"])
def log_nfc():
    uid = request.form.get("uid")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr  # 获取访问 IP

    conn = sqlite3.connect("nfc_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (uid, timestamp, ip) VALUES (?, ?, ?)", (uid, timestamp, ip))
    conn.commit()
    conn.close()

    return f"Logged NFC UID: {uid}"

# 查看日志（Web 界面）
@app.route("/view_logs")
def view_logs():
    conn = sqlite3.connect("nfc_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()

    html = "<h2>NFC 访问日志</h2><table border='1'><tr><th>ID</th><th>UID</th><th>时间</th><th>IP</th></tr>"
    for row in data:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table>"
    
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
