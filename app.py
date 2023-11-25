from flask import Flask, request, jsonify, session
import time
from openai import OpenAI
from secret import api_key  # Importing API key from secret.py
from flask_session import Session  # Import session management

client = OpenAI(api_key=api_key)

# Flask app setup
app = Flask(__name__)

# Configure the session type
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Your existing assistant ID
assistant_id = "asst_hTHe8cgWzKJnrYF8Si0OswnZ"

@app.route('/')
def index():
    if 'thread_id' not in session:
        # Create a Thread if not already present in the session
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
    return app.send_static_file('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['message']

    # Retrieve the thread ID from the session
    thread_id = session.get('thread_id', None)
    if thread_id is None:
        return jsonify({'error': 'Session expired or invalid.'}), 400

    # Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run the Assistant using the existing assistant ID
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Wait for a response from the assistant
    while True:
        time.sleep(3)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )

            # Find the assistant's response and return it
            for msg in messages.data:
                if msg.role == 'assistant':
                    content = msg.content[0].text.value
                    return jsonify({'reply': content})
                
@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    # Clear any existing session data
    session.clear()

    # Create a new Thread for a fresh start
    thread = client.beta.threads.create()
    session['thread_id'] = thread.id

    # Return a confirmation message
    return jsonify({'message': 'Conversation has been reset.'})                

if __name__ == '__main__':
    app.run(debug=True)
