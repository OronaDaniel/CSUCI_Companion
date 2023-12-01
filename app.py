from sys import displayhook
from flask import Flask, request, jsonify, session
import time
from openai import OpenAI
from secret import api_key 
from secret import api_key, assistant_id
from flask_session import Session  
import json
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MyAppLogger')

# Set up a file handler with rotation
file_handler = RotatingFileHandler('myapp.log', maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

logger.addHandler(file_handler)

client = OpenAI(api_key=api_key)

def show_json(obj):
    displayhook(json.loads(obj.model_dump_json()))

# Flask app setup
app = Flask(__name__)

# Configure the session type
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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

    # Start timer for logging API response time 
    start_time = time.time()

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
        time.sleep(2)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            
            end_time = time.time()
            duration = end_time - start_time

            messages = client.beta.threads.messages.list(thread_id=thread_id)
            show_json(messages)

            # Find the assistant's response and return it
            for msg in messages.data:
                if msg.role == 'assistant':
                    content = msg.content[0].text.value

                    # Log the duration of the API call
                    logger.info(f"User input: {user_input}\nResponse: {content}\nDuration: {duration:.2f} seconds\n")
                    return jsonify({'reply': content})
                
@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    # Clear any existing session data
    session.clear()

    # Create a new Thread for a fresh start
    thread = client.beta.threads.create()
    session['thread_id'] = thread.id

    logger.info("Conversation reset\n")

    # Return a confirmation message
    return jsonify({'message': 'Conversation has been reset.'})                

if __name__ == '__main__':
    app.run(debug=True)
