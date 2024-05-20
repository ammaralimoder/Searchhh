import os
from flask import Flask
from bot import main as bot_main

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is the Telegram bot server."

if __name__ == "__main__":
    # Start the bot in a separate thread or process
    import threading
    bot_thread = threading.Thread(target=bot_main)
    bot_thread.start()

    # Start the Flask web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
