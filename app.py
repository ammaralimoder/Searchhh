from flask import Flask
from bot import main

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
