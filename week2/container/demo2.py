import os
import pickle
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

# Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = 'credentials/token.pickle'    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available
    if not creds:
        logging.error("Credentials not found.")
        raise Exception("Credentials not found.")

    return build('drive', 'v3', credentials=creds)

def search(service, query):
    # search for the file
    result = []
    page_token = None
    while True:
        logging.info(f"Searching for files with query: {query}")
        response = service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, size)",
            pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"],
                           file["name"],
                           file["mimeType"]
                           ))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def backup_folder():
    service = get_gdrive_service()
    folder_name = "upload"
    backup_folder_name = "week2"

    # Get the backup folder ID or create it if it doesn't exist
    search_result = search(service, query=f"name='{backup_folder_name}'")
    if search_result:
        backup_folder_id = search_result[0][0]
        logging.info(f"Backup folder already present, ID: {backup_folder_id}")
    else:
        logging.info("Backup Folder not found! New Backup folder is being created...")
        file_metadata = {'name': backup_folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        backup_folder = service.files().create(body=file_metadata, fields='id').execute()
        backup_folder_id = backup_folder.get('id')
        logging.info(f"Backup folder created, ID: {backup_folder_id}")

    # Get a list of files already present in the backup folder
    backup_files = search(service, query=f"'{backup_folder_id}' in parents")

    # Upload files from the folder to the backup folder
    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        if os.path.isfile(file_path):
            # Check if the file already exists in the backup folder
            existing_file = next((file for file in backup_files if file[1] == file_name), None)
            if existing_file:
                logging.info(f"File '{file_name}' already exists in the backup folder. Skipping upload.")
            else:
                logging.info(f"Uploading file '{file_name}'...")
                file_metadata = {"name": file_name, "parents": [backup_folder_id]}
                media = MediaFileUpload(file_path, resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                logging.info(f"File uploaded: {file_name}, ID: {file.get('id')}")
    logging.info("Backup completed")

if __name__ == '__main__':
    # while True:
    #     backup_folder()
    #     time.sleep(10)  # Wait
    backup_folder()
    time.sleep(150)