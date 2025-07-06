from flask import Flask, request, render_template, jsonify
from instagrapi import Client
import os
import time
import threading

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Offline Loader</title>

    <!-- Google Fonts for better typography -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

    <!-- Inline CSS for styling -->
    <style>
        /* Basic reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #6f7fff, #4CAF50);
            color: #fff;
            padding: 30px;
            background-size: 400% 400%;
            animation: gradientAnimation 10s ease infinite;
        }

        /* Gradient animation for the background */
        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        h1 {
            text-align: center;
            font-size: 42px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        }

        h3 {
            text-align: center;
            font-size: 24px;
            color: #f39c12;
            margin-bottom: 20px;
            font-weight: 600;
        }

        /* Container to hold the form */
        .form-container {
            background-color: #fff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
            max-width: 600px;
            margin: 0 auto;
            overflow: hidden;
            transform: scale(1);
            transition: transform 0.3s ease;
        }

        .form-container:hover {
            transform: scale(1.05);
        }

        .form-container input,
        .form-container select,
        .form-container button {
            width: 100%;
            padding: 16px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 16px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }

        .form-container input[type="file"] {
            padding: 10px;
            cursor: pointer;
        }

        .form-container button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .form-container button:hover {
            background-color: #45a049;
        }

        .form-container input:focus,
        .form-container select:focus,
        .form-container button:focus {
            outline: none;
            border-color: #4CAF50;
        }

        /* Form label styling */
        .form-container label {
            font-size: 16px;
            color: #555;
            margin-bottom: 5px;
            text-transform: uppercase;
        }

        /* Message display */
        .message {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            color: #e74c3c;
            margin-top: 20px;
        }

        /* Icon in button */
        .form-container button i {
            margin-right: 10px;
        }

        /* Animated input borders */
        .form-container input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
        }

        /* Glow effect on form fields */
        .form-container input,
        .form-container select,
        .form-container button {
            transition: box-shadow 0.3s ease;
        }

        .form-container input:focus,
        .form-container select:focus,
        .form-container button:hover {
            box-shadow: 0 0 12px rgba(76, 175, 80, 0.8);
        }

        /* Responsive design */
        @media (max-width: 600px) {
            .form-container {
                padding: 20px;
            }

            h1 {
                font-size: 28px;
            }

            .form-container input,
            .form-container button {
                padding: 12px;
            }
        }
    </style>
</head>
<body>

    <h1>LEGEND MALICK INSTAGRAM LOADER</h1>

    <!-- Display success or processing message -->
    {% if message %}
        <h3>{{ message }}</h3>
    {% endif %}

    <!-- Form Container -->
    <div class="form-container">
        <form action="/" method="POST" enctype="multipart/form-data">
            
            <label for="username">Instagram Username:</label>
            <input type="text" name="username" required placeholder="Enter Instagram Username" />

            <label for="password">Instagram Password:</label>
            <input type="password" name="password" required placeholder="Enter Instagram Password" />

            <label for="recipient">Target Username</label>
            <input type="text" name="recipient" required placeholder="Enter Username or Group Name" />

            <label for="interval">Interval (in seconds):</label>
            <input type="number" name="interval" required placeholder="Enter Interval (seconds)" />

            <label for="haters_name">Hater's Name:</label>
            <input type="text" name="haters_name" required placeholder="Enter Hater's Name" />

            <label for="message_file">Upload Message File:</label>
            <input type="file" name="message_file" required />

            <!-- Submit button with an icon -->
            <button type="submit">
                <i class="fas fa-paper-plane"></i> Start Sending Messages
            </button>
        </form>
    </div>

    <!-- FontAwesome CDN for the paper plane icon -->
    <script src="https://kit.fontawesome.com/a076d05399.js"></script>
</body>
</html>
def send_messages_from_file(username, password, recipient, message_file, interval, haters_name, result_callback):
    cl = Client()
    try:

        cl.login(username, password)
        print("Logged in successfully!")

        recipient_id = None

        try:
            recipient_id = cl.user_id_from_username(recipient)
            if not recipient_id:
                raise ValueError("Recipient username not found!")
            print(f"Recipient username found: {recipient}")
        except Exception:
            try:
            	
                recipient_id = cl.chat_id_from_name(recipient)
                if not recipient_id:
                    raise ValueError("Group name not found!")
                print(f"Group found: {recipient}")
            except Exception:
                print("Neither username nor group found!")
                return "Recipient username or group not found!"

        with open(message_file, 'r') as file:
            messages = file.readlines()

        for message in messages:
            message = message.strip()
            if message:
                try:
                	
                    formatted_message = f"{haters_name} {message}"

                    if recipient_id:
                        if 'group' in recipient.lower(): 
                            cl.chat_send_message(recipient_id, formatted_message)
                            print(f"Message sent to group: {formatted_message}")
                        else:
                            cl.direct_send(formatted_message, [recipient_id])
                            print(f"Message sent to user: {formatted_message}")
                except Exception as e:
                    print(f"Failed to send message: {formatted_message}. Error: {e}")

            time.sleep(interval)

    except Exception as e:
        print(f"Error: {e}")
        return str(e)

    return "All messages sent successfully!"

def handle_user_request(username, password, recipient, message_file, interval, haters_name, result_callback):
    result = send_messages_from_file(username, password, recipient, message_file, interval, haters_name, result_callback)
    result_callback(result)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        recipient = request.form["recipient"]
        interval = int(request.form["interval"])
        haters_name = request.form["haters_name"]

        if "message_file" not in request.files:
            return "No message file uploaded!"
        
        file = request.files["message_file"]
        if file.filename == "":
            return "No selected file!"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        def result_callback(result):
            return render_template("index.html", message=result)

        thread = threading.Thread(target=handle_user_request, args=(username, password, recipient, file_path, interval, haters_name, result_callback))
        thread.start()

        return render_template("index.html", message="Processing your request... Please wait!")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
