from flask import Flask, request, jsonify
import requests
import time
import threading

app = Flask(__name__)

BASE_URL = "https://i.instagram.com/api/v1/"
USER_AGENT = "Instagram 123.0.0.21.114 Android"
sending_thread = None
stop_sending = False


def login_with_cookie(cookie):
    """
    Log in to Instagram using a provided cookie.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": cookie,
    }
    response = requests.get(BASE_URL + "accounts/current_user/", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get("user", {}).get("username", "Unknown"), headers
    else:
        return None, None


def get_user_id(headers, username):
    """
    Get the user ID from the username.
    """
    url = BASE_URL + f"users/web_profile_info/?username={username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get("data", {}).get("user", {}).get("id")
    return None


def send_message(headers, recipient_id, messages, delay, haters_name, is_group):
    """
    Send messages to a specified Instagram recipient (group or user) repeatedly with a delay.
    """
    global stop_sending
    message_url = BASE_URL + "direct_v2/threads/broadcast/text/"

    for message in messages:
        if stop_sending:
            break

        full_message = f"{haters_name} {message}"
        if is_group:
            payload = {
                "thread_ids": f"[{recipient_id}]",
                "text": full_message,
            }
        else:
            payload = {
                "recipient_users": f"[{recipient_id}]",
                "text": full_message,
            }

        response = requests.post(message_url, headers=headers, data=payload)
        if response.status_code == 200:
            print(f"Message sent: {full_message}")
        else:
            print(f"Failed to send message: {response.text}")
        time.sleep(delay)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global sending_thread, stop_sending
        stop_sending = False
        cookie = request.form.get("cookie")
        target = request.form.get("target")
        is_group = request.form.get("is_group") == "true"
        delay = float(request.form.get("delay", 5))
        haters_name = request.form.get("haters_name")
        message_file = request.files.get("message_file")

        # Verify login
        username, headers = login_with_cookie(cookie)
        if not username:
            return jsonify({"success": False, "message": "Invalid cookie. Login failed."})

        # Get recipient ID
        if is_group:
            recipient_id = target  # Use group ID directly
        else:
            recipient_id = get_user_id(headers, target)
            if not recipient_id:
                return jsonify({"success": False, "message": "Invalid username. User not found."})

        # Parse message file
        messages = message_file.read().decode("utf-8").splitlines()

        # Start the messaging thread
        sending_thread = threading.Thread(
            target=send_message, args=(headers, recipient_id, messages, delay, haters_name, is_group)
        )
        sending_thread.start()

        return jsonify({"success": True, "message": f"Logged in as {username}. Messaging started."})

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Messaging</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(to right, #6a11cb, #2575fc);
                color: #fff;
            }

            .container {
                max-width: 600px;
                margin: 50px auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }

            h1 {
                text-align: center;
                margin-bottom: 20px;
            }

            form {
                display: flex;
                flex-direction: column;
            }

            label {
                margin-top: 10px;
                font-weight: bold;
            }

            input, select, textarea {
                margin-top: 5px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }

            input[type="file"] {
                padding: 5px;
                background: #fff;
            }

            button {
                margin-top: 20px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background: #2575fc;
                color: white;
                font-size: 18px;
                cursor: pointer;
                transition: background 0.3s;
            }

            button:hover {
                background: #6a11cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Instagram Auto Messaging</h1>
            <form id="messagingForm" method="POST" enctype="multipart/form-data">
                <label for="cookie">Instagram Cookie:</label>
                <input type="text" id="cookie" name="cookie" placeholder="Enter Instagram Cookie" required>

                <label for="haters_name">Hater's Name:</label>
                <input type="text" id="haters_name" name="haters_name" placeholder="Enter Hater's Name" required>

                <label for="target">Target Group ID or Username:</label>
                <input type="text" id="target" name="target" placeholder="Enter Group ID or Username" required>

                <label for="is_group">Is this a group? (Yes/No):</label>
                <select id="is_group" name="is_group">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>

                <label for="delay">Delay (seconds):</label>
                <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

                <label for="message_file">Message File (txt):</label>
                <input type="file" id="message_file" name="message_file" accept=".txt" required>

                <button type="submit">Start Messaging</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route("/stop", methods=["POST"])
def stop_sending_messages():
    global stop_sending
    stop_sending = True
    return jsonify({"success": True, "message": "Message sending stopped."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
