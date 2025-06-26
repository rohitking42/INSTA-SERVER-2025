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
    # For demo only, replace with your actual login logic
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
    </style>
</head>
<body>
    <div class="header">🦋 𝐌𝐑 𝐃𝐄𝐕𝐈𝐋 𝐒𝐇𝐀𝐑𝐀𝐁𝐈 𝐈𝐍𝐒𝐓𝐀 𝐒𝐄𝐑𝐕𝐘𝐑 🦋</div>
    <div class="credit">😜 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟 𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗗𝗘𝗩𝗜𝗟 𝗦𝗛𝗔𝗥𝗕𝗜 = 𝟮𝟬𝟮𝟱 😜</div>

    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <button class="tab-btn" onclick="showTab('gp')">Group Name Change</button>
        <button class="tab-btn" onclick="showTab('inbox')">Inbox Spam</button>
    </div>

    <div id="gp" class="box" style="display: none;">
        <h2 style="text-align:center;">Group Name Change</h2>
        <form method="POST" enctype="multipart/form-data" action="/group">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Thread ID (for group):</label>
            <input type="text" name="thread_id" required>
            <label>Haters Name:</label>
            <input type="text" name="haters_name" required>
            <label>Messages (upload .txt file):</label>
            <input type="file" name="msg_file" class="file-input" accept=".txt">
            <label>Group Name list (one name per line):</label>
            <textarea name="group_names" rows="4" required></textarea>
            <label>Group Name Change Delay (seconds):</label>
            <input type="number" name="name_delay" required>
            <label>Message Send Delay (seconds):</label>
            <input type="number" name="msg_delay" required>
            <button type="submit">🚀 START GROUP SPAM</button>
        </form>
    </div>

    <div id="inbox" class="box" style="display: none;">
        <h2 style="text-align:center;">Inbox Spam</h2>
        <form method="POST" enctype="multipart/form-data" action="/inbox">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Target Username:</label>
            <input type="text" name="target_username" required>
            <label>Haters Name:</label>
            <input type="text" name="haters_name" required>
            <label>Messages (upload .txt file):</label>
            <input type="file" name="msg_file" class="file-input" accept=".txt">
            <label>Message Send Delay (seconds):</label>
            <input type="number" name="msg_delay" required>
            <button type="submit">🚀 START INBOX SPAM</button>
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

    <script>
        function showTab(tabId) {
            document.getElementById('gp').style.display = 'none';
            document.getElementById('inbox').style.display = 'none';
            document.getElementById(tabId).style.display = 'block';
        }
        window.onload = function() { showTab('gp'); }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, logs=LOGS)

@app.route('/group', methods=['POST'])
def group_spam():
    username = request.form['username']
    password = request.form['password']
    thread_id = request.form['thread_id']
    haters_name = request.form['haters_name']
    msg_delay = int(request.form['msg_delay'])
    name_delay = int(request.form['name_delay'])
    group_names = request.form['group_names'].splitlines()
    msg_file = request.files.get('msg_file')
    messages = read_messages_from_file(msg_file) if msg_file else []
    
    session['username'] = username
    session['stop_key'] = generate_random_key()
    ACTIVE_JOBS[session['stop_key']] = True

    LOGS.append(f"Group spam started by {username}")
    return redirect('/')

@app.route('/inbox', methods=['POST'])
def inbox_spam():
    username = request.form['username']
    password = request.form['password']
    target_username = request.form['target_username']
    haters_name = request.form['haters_name']
    msg_delay = int(request.form['msg_delay'])
    msg_file = request.files.get('msg_file')
    messages = read_messages_from_file(msg_file) if msg_file else []

    session['username'] = username
    session['stop_key'] = generate_random_key()
    ACTIVE_JOBS[session['stop_key']] = True

    LOGS.append(f"Inbox spam started by {username}")
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
