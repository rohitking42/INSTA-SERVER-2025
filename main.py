import os
import time
import random
import string
from flask import Flask, render_template_string, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = "your_ultra_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'

LOGS = []
ACTIVE_JOBS = {}

def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def instagram_login(username, password):
    # Replace with actual login logic
    return True

def read_messages_from_file(file):
    if file and file.filename.endswith('.txt'):
        return file.read().decode('utf-8').splitlines()
    return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦋 MR DEVIL SHARABI INSTA SERVER 🦋</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(45deg, #ff00cc, #3300ff);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #fff;
        }
        .header {
            font-size: 1.8rem;
            margin: 20px 0 10px;
            text-align: center;
            color: #fff;
            text-shadow: 0 0 8px #ff00cc;
        }
        .credit {
            font-size: 1rem;
            margin: 0 0 20px;
            color: #fff;
            text-align: center;
        }
        .tab-btn {
            background: linear-gradient(45deg, #ff00cc, #3300ff);
            color: #fff;
            border: none;
            padding: 12px 24px;
            margin: 8px;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .active-tab {
            background: #fff;
            color: #ff00cc;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .box {
            background: rgba(0,0,0,0.7);
            border: 2px solid #ff00cc;
            border-radius: 20px;
            padding: 20px;
            width: 90%;
            max-width: 500px;
            margin-bottom: 20px;
        }
        input, textarea, select, button, .file-input {
            width: 100%;
            padding: 12px;
            margin: 12px 0;
            font-size: 1rem;
            border-radius: 10px;
            border: 1px solid #ff00cc;
            background: rgba(0,0,0,0.5);
            color: #fff;
        }
        button {
            background: linear-gradient(45deg, #ff00cc, #3300ff);
            color: #fff;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .log-box {
            background: rgba(0,0,0,0.7);
            border-radius: 20px;
            padding: 15px;
            width: 90%;
            max-width: 500px;
            height: 200px;
            overflow-y: scroll;
            border: 2px solid #ff00cc;
            color: #fff;
            font-family: monospace;
            margin-bottom: 20px;
        }
        .log-line {
            margin: 5px 0;
        }
        .flash-msg {
            color: #ff4444;
            margin: 10px 0;
            text-align: center;
        }
        .stop-btn {
            background: linear-gradient(45deg, #ff4444, #ff00cc);
        }
        .user-session {
            color: #fff;
            margin-top: 10px;
            text-align: center;
        }
        .footer {
            font-size: 0.9rem;
            color: #fff;
            margin: 15px 0;
            text-align: center;
        }
        .footer a {
            color: #ff00cc;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="header">🦋 𝐌𝐑 𝐃𝐄𝐕𝐈𝐋 𝐒𝐇𝐀𝐑𝐀𝐁𝐈 𝐈𝐍𝐒𝐓𝐀 𝐒𝐄𝐑𝐕𝐘𝐑 🦋</div>
    <div class="credit">😜 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟 𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗗𝗘𝗩𝐈𝐋 𝗦𝗛𝗔𝐑𝐁𝐈 = 𝟮𝟬𝟮𝟱 😜</div>

    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <button class="tab-btn" onclick="showTab('gp_name')">Group Name Change</button>
        <button class="tab-btn" onclick="showTab('inbox_name')">Inbox Name Change</button>
    </div>

    <div id="gp_name" class="box" style="display: none;">
        <h2 style="text-align:center;">Group Name Change</h2>
        <form method="POST" enctype="multipart/form-data" action="/gp_name">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Thread ID (for group):</label>
            <input type="text" name="thread_id" required>
            <label>Group Name List (one name per line):</label>
            <textarea name="group_names" rows="4" required></textarea>
            <label>Group Name Change Delay (seconds):</label>
            <input type="number" name="name_delay" required>
            <button type="submit">🚀 START GROUP NAME CHANGE</button>
        </form>
    </div>

    <div id="inbox_name" class="box" style="display: none;">
        <h2 style="text-align:center;">Inbox Name Change</h2>
        <form method="POST" enctype="multipart/form-data" action="/inbox_name">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Target Username:</label>
            <input type="text" name="target_username" required>
            <label>Inbox Name List (one name per line):</label>
            <textarea name="inbox_names" rows="4" required></textarea>
            <label>Name Change Delay (seconds):</label>
            <input type="number" name="name_delay" required>
            <button type="submit">🚀 START INBOX NAME CHANGE</button>
        </form>
    </div>

    <div class="box">
        <h2 style="text-align:center;">Message Spam</h2>
        <form method="POST" enctype="multipart/form-data" action="/msg_spam">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Thread ID (for group) or Target Username (for inbox):</label>
            <input type="text" name="target" required>
            <label>Type:</label>
            <select name="type" required>
                <option value="group">Group</option>
                <option value="inbox">Inbox</option>
            </select>
            <label>Haters Name:</label>
            <input type="text" name="haters_name" required>
            <label>Messages (upload .txt file):</label>
            <input type="file" name="msg_file" class="file-input" accept=".txt">
            <label>Message Send Delay (seconds):</label>
            <input type="number" name="msg_delay" required>
            <button type="submit">🚀 START MESSAGE SPAM</button>
        </form>
    </div>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="flash-msg">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="log-box">
        {% for log in logs %}
            <div class="log-line">{{ log }}</div>
        {% endfor %}
        {% if session.get('username') %}
            <div class="user-session">User: {{ session['username'] }}</div>
        {% endif %}
    </div>

    {% if session.get('stop_key') %}
        <div class="box" style="text-align: center;">
            <h3>Stop Key: {{ session['stop_key'] }}</h3>
            <form method="POST" action="/stop">
                <input type="text" name="stop_key" placeholder="Enter Stop Key" required>
                <button type="submit" class="stop-btn">STOP SPAM</button>
            </form>
        </div>
    {% endif %}

    <div class="footer">
        😜 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟 𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗗𝗘𝗩𝐈𝐋 𝗦𝗛𝗔𝐑𝐁𝐈 = 𝟮𝟬𝟮𝟱 😜<br>
        🙈 𝗔𝗡𝗬 𝗞𝗜𝗡𝗗 𝗛𝗘𝗟𝗣 𝗠𝗥 𝗗𝗘𝗩𝐈𝐋 𝗪𝗣 𝗡𝗢 = 𝟵𝟬𝟮𝟰𝟴𝟳𝟬𝟰𝟱𝟲 🙈<br>
        <a href="https://www.facebook.com/share/1J5MGGccW1/" target="_blank">My Facebook Profile</a>
    </div>

    <script>
        function showTab(tabId) {
            document.getElementById('gp_name').style.display = 'none';
            document.getElementById('inbox_name').style.display = 'none';
            document.getElementById(tabId).style.display = 'block';
        }
        window.onload = function() { showTab('gp_name'); }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, logs=LOGS)

@app.route('/gp_name', methods=['POST'])
def group_name_change():
    username = request.form['username']
    password = request.form['password']
    thread_id = request.form['thread_id']
    group_names = request.form['group_names'].splitlines()
    name_delay = int(request.form['name_delay'])

    session['username'] = username
    session['stop_key'] = generate_random_key()
    ACTIVE_JOBS[session['stop_key']] = True

    LOGS.append(f"Group name change started by {username}")
    return redirect('/')

@app.route('/inbox_name', methods=['POST'])
def inbox_name_change():
    username = request.form['username']
    password = request.form['password']
    target_username = request.form['target_username']
    inbox_names = request.form['inbox_names'].splitlines()
    name_delay = int(request.form['name_delay'])

    session['username'] = username
    session['stop_key'] = generate_random_key()
    ACTIVE_JOBS[session['stop_key']] = True

    LOGS.append(f"Inbox name change started by {username}")
    return redirect('/')

@app.route('/msg_spam', methods=['POST'])
def msg_spam():
    username = request.form['username']
    password = request.form['password']
    target = request.form['target']
    type_ = request.form['type']
    haters_name = request.form['haters_name']
    msg_delay = int(request.form['msg_delay'])
    msg_file = request.files.get('msg_file')
    messages = read_messages_from_file(msg_file) if msg_file else []

    session['username'] = username
    session['stop_key'] = generate_random_key()
    ACTIVE_JOBS[session['stop_key']] = True

    LOGS.append(f"Message spam started by {username} (Type: {type_}, Target: {target})")
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop_spam():
    stop_key = request.form['stop_key']
    if stop_key in ACTIVE_JOBS:
        ACTIVE_JOBS[stop_key] = False
        LOGS.append(f"Spam stopped with key: {stop_key}")
        session.pop('stop_key', None)
    else:
        flash("Invalid stop key!")
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
