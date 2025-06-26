import os
import time
import random
import string
from flask import Flask, render_template_string, request, redirect, flash, session
from instagrapi import Client

app = Flask(__name__)
app.secret_key = "your_ultra_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'

LOGS = []
ACTIVE_JOBS = {}

def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def instagram_login(username, password):
    cl = Client()
    try:
        cl.login(username, password)
        return cl
    except Exception as e:
        return str(e)

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
            display: none;
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
            background: linear-gradient(45deg, #ff4444, #3300ff);
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
        .close-btn {
            background: #ff4444;
            color: #fff;
            border: none;
            border-radius: 50px;
            padding: 8px 16px;
            margin: 8px;
            font-weight: bold;
            cursor: pointer;
        }
        .msg-box {
            background: rgba(0,0,0,0.7);
            border: 2px solid #ff00cc;
            border-radius: 20px;
            padding: 20px;
            width: 90%;
            max-width: 500px;
            margin-bottom: 20px;
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
        <button class="close-btn" onclick="hideTab('gp_name')">✖ Close</button>
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
        <button class="close-btn" onclick="hideTab('inbox_name')">✖ Close</button>
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

    <div class="msg-box">
        <h2 style="text-align:center;">Message Auto Sender Tool</h2>
        <form method="POST" enctype="multipart/form-data" action="/msg_spam">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            <label>Target Type:</label>
            <select name="type" required>
                <option value="group">Group</option>
                <option value="inbox">Inbox</option>
            </select>
            <label>Target Username (for inbox):</label>
            <input type="text" name="target_username">
            <label>Thread ID (for group):</label>
            <input type="text" name="thread_id">
            <label>Haters Name:</label>
            <input type="text" name="haters_name" required>
            <label>Messages (Ek ek line m likho):</label>
            <textarea name="messages" rows="4"></textarea>
            <label>Messages (upload .txt file):</label>
            <input type="file" name="msg_file" class="file-input" accept=".txt">
            <label>Group Name Change Count:</label>
            <input type="number" name="change_count">
            <label>Group Name List (Har ek name alag line m):</label>
            <textarea name="group_names" rows="4"></textarea>
            <label>Group Name Change Delay (seconds):</label>
            <input type="number" name="name_delay">
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
        function hideTab(tabId) {
            document.getElementById(tabId).style.display = 'none';
        }
        // Start with all tabs closed except message box
        document.getElementById('gp_name').style.display = 'none';
        document.getElementById('inbox_name').style.display = 'none';
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, logs=LOGS)

@app.route('/gp_name', methods=['POST'])
def group_name_change():
    try:
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
    except Exception as e:
        flash(f"Error: {e}")
        return redirect('/')

@app.route('/inbox_name', methods=['POST'])
def inbox_name_change():
    try:
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
    except Exception as e:
        flash(f"Error: {e}")
        return redirect('/')

@app.route('/msg_spam', methods=['POST'])
def msg_spam():
    try:
        username = request.form['username']
        password = request.form['password']
        type_ = request.form['type']
        haters_name = request.form['haters_name']
        msg_delay = int(request.form['msg_delay'])
        msg_file = request.files.get('msg_file')
        messages = []
        if msg_file and msg_file.filename.endswith('.txt'):
            messages = msg_file.read().decode('utf-8').splitlines()
        else:
            messages = request.form['messages'].splitlines()
        if not messages:
            flash("Please enter messages or upload a valid .txt file!")
            return redirect('/')

        group_names = request.form.get('group_names', '').splitlines()
        change_count = int(request.form.get('change_count', 0))
        name_delay = int(request.form.get('name_delay', 0))
        thread_id = request.form.get('thread_id', '')
        target_username = request.form.get('target_username', '')

        session['username'] = username
        session['stop_key'] = generate_random_key()
        ACTIVE_JOBS[session['stop_key']] = True

        cl = instagram_login(username, password)
        if isinstance(cl, str):
            flash(f"Login failed: {cl}")
            return redirect('/')

        if type_ == "inbox":
            try:
                user_id = cl.user_id_from_username(target_username)
                LOGS.append(f"Inbox spam started by {username} (Target: {target_username})")
                while ACTIVE_JOBS.get(session['stop_key'], True):
                    for msg in messages:
                        full_msg = f"{haters_name} {msg}"
                        cl.direct_send(full_msg, [user_id])
                        LOGS.append(f"Message sent: {full_msg}")
                        time.sleep(msg_delay)
            except Exception as e:
                flash(f"Inbox msg error: {e}")
                return redirect('/')
        elif type_ == "group":
            try:
                LOGS.append(f"Group spam started by {username} (Thread: {thread_id})")
                big_msg = f"{haters_name} {' '.join(messages)}"
                cl.direct_send(big_msg, thread_ids=[thread_id])
                time.sleep(msg_delay)
                for i in range(min(change_count, len(group_names))):
                    new_name = group_names[i]
                    cl.group_edit(thread_id, new_name)
                    LOGS.append(f"Group name changed to: {new_name}")
                    time.sleep(name_delay)
                while ACTIVE_JOBS.get(session['stop_key'], True):
                    for msg in messages:
                        full_msg = f"{haters_name} {msg}"
                        cl.direct_send(full_msg, thread_ids=[thread_id])
                        LOGS.append(f"Message sent: {full_msg}")
                        time.sleep(msg_delay)
            except Exception as e:
                flash(f"Group msg error: {e}")
                return redirect('/')
        else:
            flash("Invalid choice!")
            return redirect('/')
        return redirect('/')
    except Exception as e:
        flash(f"Internal error: {e}")
        return redirect('/')

@app.route('/stop', methods=['POST'])
def stop_spam():
    try:
        stop_key = request.form['stop_key']
        if stop_key in ACTIVE_JOBS:
            ACTIVE_JOBS[stop_key] = False
            LOGS.append(f"Spam stopped with key: {stop_key}")
            session.pop('stop_key', None)
        else:
            flash("Invalid stop key!")
        return redirect('/')
    except Exception as e:
        flash(f"Error: {e}")
        return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
