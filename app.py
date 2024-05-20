import os
import logging
import requests
import zipfile
from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

DATA_URL = os.getenv('DATA_URL')  # URL to download the data file (could be a zip file)

def download_and_extract_data(url, extract_to='.'):
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(extract_to, local_filename)
    
    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Check if the response contains a zip file
    if 'zip' in response.headers.get('Content-Type', ''):
        # If it's a zip file, extract it
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        # Assuming the extracted file is named 'data.txt'
        extracted_file_path = os.path.join(extract_to, 'data.txt')
        return extracted_file_path
    else:
        # If it's not a zip file, save it directly
        with open(local_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_filepath

# Load data from text file into a list of lists
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip().split(','))
    return data

# Initialize data
data = []

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a query and I will return the corresponding data.')

def query(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    response = ""
    for row in data:
        if query in row:
            response = ','.join(row)
            break
    if response:
        update.message.reply_text(response)
    else:
        update.message.reply_text('No data found for your query.')

def main():
    global data
    
    # Download and load data
    data_file_path = download_and_extract_data(DATA_URL)
    data = load_data(data_file_path)
    
    # Set up the Updater
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("query", query))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()
  
