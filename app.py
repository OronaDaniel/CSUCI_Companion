from flask import Flask, request, jsonify, session
import time
from openai import OpenAI
from secret import api_key  # Importing API key from secret.py
from flask_session import Session  # Import session management
import json

assistant_id = "asst_hTHe8cgWzKJnrYF8Si0OswnZ"

client = OpenAI(api_key=api_key)

def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


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

    # add message to thread from user input
    message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
    show_json(message)

    # create the asynchronous run
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    show_json(run)

    # sleep every 0.5s to check status
    while True:
        time.sleep(0.5)

        # retrieve status
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        show_json(run)

        # if status is completed 
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc", after=message.id)
            show_json(messages)
            pretty_print(messages)

            # Find the assistant's response and return it
            for msg in messages.data:
                if msg.role == 'assistant':
                    content = msg.content[0].text.value
                    return jsonify({'reply': content})

if __name__ == '__main__':
    app.run(debug=True)
