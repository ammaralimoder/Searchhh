import os
import logging
import requests
import py7zr
from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

DATA_URL = os.getenv('DATA_URL')  # URL to download the data file (could be a .7z file)

# Status flag to track data download and extraction
data_status = {"downloaded": False}

# Function to download and extract .7z data
def download_and_extract_data(url, extract_to='.'):
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(extract_to, local_filename)
    
    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    if '7z' in response.headers.get('Content-Type', '') or local_filename.endswith('.7z'):
        with py7zr.SevenZipFile(BytesIO(response.content)) as archive:
            archive.extractall(path=extract_to)
        extracted_files = [
            os.path.join(extract_to, 'مصر - الجزء الأول.txt'),
            os.path.join(extract_to, 'مصر - الجزء الثاني.txt'),
            os.path.join(extract_to, 'مصر - الجزء الثالث.txt'),
            os.path.join(extract_to, 'مصر - الجزء الرابع.txt')
        ]
        return extracted_files
    else:
        with open(local_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return [local_filepath]

# Load data from multiple text files into a list of lists
def load_data(file_paths):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(line.strip().split(','))
    return data

# Initialize data
data = []

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a query and I will return the corresponding data. Use /query <your_search_term>. Use /status to check if data is ready.')

def query(update: Update, context: CallbackContext) -> None:
    query_text = ' '.join(context.args)
    response = ""
    for row in data:
        if query_text in row:
            response = ','.join(row)
            break
    if response:
        update.message.reply_text(response)
    else:
        update.message.reply_text('No data found for your query.')

def status(update: Update, context: CallbackContext) -> None:
    if data_status["downloaded"]:
        update.message.reply_text('Data files are downloaded and extracted.')
    else:
        update.message.reply_text('Data files are not yet downloaded and extracted.')

def main():
    global data, data_status
    
    # Download and load data
    data_file_paths = download_and_extract_data(DATA_URL)
    data = load_data(data_file_paths)
    
    # Update the status flag
    data_status["downloaded"] = True
    
    # Set up the Updater
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Handlers for the start, query, and status commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("query", query, pass_args=True))
    dispatcher.add_handler(CommandHandler("status", status))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()
    
