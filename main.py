import os
import time
from flask import Flask, render_template_string, request, redirect, flash, url_for
from instagrapi import Client

app = Flask(__name__)
app.secret_key = "your_secret_key"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>🐉 DRAGON INSTA GROUP SPAMMER 🩷</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, pink, skyblue);
            color: green;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: yellow;
            padding: 20px;
            border-radius: 15px;
            width: 90%;
            max-width: 500px;
        }
        input, textarea, select, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            background-color: green;
            color: white;
            font-weight: bold;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2 style="text-align:center;">🐉 DRAGON INSTAGRAM SPAMMER PANEL 🩷</h2>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <p style="color:red;">{{ message }}</p>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form method="POST">
            <label>Instagram Username:</label>
            <input type="text" name="username" required>
            
            <label>Instagram Password:</label>
            <input type="password" name="password" required>
            
            <label>Target Type:</label>
            <select name="choice" required>
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
            <textarea name="messages" rows="4" required></textarea>
            
            <label>Message Send Delay (seconds):</label>
            <input type="number" name="msg_delay" required>

            <button type="submit">🚀 START SPAM</button>
        </form>
    </div>
</body>
</html>
"""

def instagram_login(username, password):
    cl = Client()
    try:
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
        cl.login(username, password)
        cl.dump_settings("session.json")
        return cl
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        choice = request.form['choice']
        haters_name = request.form['haters_name']
        msg_delay = int(request.form['msg_delay'])
        messages = request.form['messages'].splitlines()

        cl = instagram_login(username, password)
        if isinstance(cl, str):
            flash(f"Login failed: {cl}")
            return redirect(url_for('index'))

        if choice == "inbox":
            target_username = request.form['target_username']
            try:
                user_id = cl.user_id_from_username(target_username)
                while True:
                    for msg in messages:
                        full_msg = f"{haters_name} {msg}"
                        cl.direct_send(full_msg, [user_id])
                        time.sleep(msg_delay)
            except Exception as e:
                flash(f"Inbox msg error: {e}")
                return redirect(url_for('index'))

        elif choice == "group":
            thread_id = request.form['thread_id']
            try:
                while True:
                    for msg in messages:
                        full_msg = f"{haters_name} {msg}"
                        cl.direct_send(full_msg, thread_ids=[thread_id])
                        time.sleep(msg_delay)
            except Exception as e:
                flash(f"Group msg error: {e}")
                return redirect(url_for('index'))
        else:
            flash("Invalid choice!")
            return redirect(url_for('index'))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
