import os
import logging
import boto3
import py7zr
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize boto3 client for Stackhero S3
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('STACKHERO_S3_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('STACKHERO_S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('STACKHERO_S3_SECRET_ACCESS_KEY'),
    region_name=os.getenv('STACKHERO_S3_REGION_NAME')
)

# Bucket name where the data is stored
BUCKET_NAME = os.getenv('STACKHERO_S3_BUCKET_NAME')

# Function to download data from S3 and extract .7z files
def download_and_extract_data_from_s3(s3_key, extract_to='/tmp'):
    try:
        local_filename = s3_key.split('/')[-1]
        local_filepath = os.path.join(extract_to, local_filename)
        
        # Download the .7z file from S3
        s3_client.download_file(BUCKET_NAME, s3_key, local_filepath)
        logger.info(f"Downloaded {s3_key} from S3 to {local_filepath}")
        
        # Extract the .7z file
        with py7zr.SevenZipFile(local_filepath, mode='r') as archive:
            archive.extractall(path=extract_to)
        logger.info(f"Extracted {local_filepath} to {extract_to}")
        
        # Return the paths to the extracted files
        extracted_files = [
            os.path.join(extract_to, 'مصر - الجزء الأول.txt'),
            os.path.join(extract_to, 'مصر - الجزء الثاني.txt'),
            os.path.join(extract_to, 'مصر - الجزء الثالث.txt'),
            os.path.join(extract_to, 'مصر - الجزء الرابع.txt')
        ]
        return extracted_files
    except NoCredentialsError:
        logger.error("Credentials not available for S3")

# Initialize data
data = []

# ... (rest of the bot code remains the same)

if __name__ == '__main__':
    main()
    
