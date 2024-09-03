from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from pyrogram import Client

# Flask app setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Define the folder to temporarily save session files for download
TEMP_FOLDER = "temp_sessions"

# Ensure the temp folder exists
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Your Telegram API credentials
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        if not phone_number:
            flash('Please enter a phone number!', 'error')
            return redirect(url_for('index'))

        session_name = os.path.join(TEMP_FOLDER, f"{phone_number}.session")
        
        try:
            app = Client(session_name, api_id=API_ID, api_hash=API_HASH)
            app.start()
            flash(f'Session created for {phone_number}', 'success')
            app.stop()

            # Provide download link to the user
            return send_file(session_name, as_attachment=True)
        
        except Exception as e:
            flash(str(e), 'error')

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
