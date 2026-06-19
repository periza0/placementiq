import io
import os
import pickle
import mimetypes

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

ROOT_FOLDER_ID = "152vW7rzZSTzCapE6gw665cpHMUMhDz2F"

DOWNLOAD_DIR = "data"


EXPORT_TYPES = {
    "application/vnd.google-apps.document":
        ("application/pdf", ".pdf"),

    "application/vnd.google-apps.spreadsheet":
        (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xlsx"
        ),

    "application/vnd.google-apps.presentation":
        ("application/pdf", ".pdf"),
}
def authenticate():

    creds = None

    if os.path.exists("token.pickle"):

        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(
        "drive",
        "v3",
        credentials=creds
    )
def download_binary_file(service, file_id, save_path):
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    with open(save_path, "wb") as f:
        f.write(fh.getvalue())


def export_google_file(service, file_id, export_mime, save_path):
    request = service.files().export_media(
        fileId=file_id,
        mimeType=export_mime
    )

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    with open(save_path, "wb") as f:
        f.write(fh.getvalue())


def sync_folder(service, folder_id, local_folder):

    os.makedirs(local_folder, exist_ok=True)

    page_token = None

    while True:

        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id,name,mimeType)",
            pageToken=page_token
        ).execute()

        files = results.get("files", [])

        for file in files:

            file_id = file["id"]
            file_name = file["name"]
            mime = file["mimeType"]

            # Folder
            if mime == "application/vnd.google-apps.folder":

                print(f"\n📁 Entering {file_name}")

                sync_folder(
                    service,
                    file_id,
                    os.path.join(local_folder, file_name)
                )

                continue

            # Google Docs / Sheets / Slides
            if mime in EXPORT_TYPES:

                export_mime, extension = EXPORT_TYPES[mime]

                save_path = os.path.join(
                    local_folder,
                    file_name + extension
                )

                print(f"📄 Exporting {file_name}")

                export_google_file(
                    service,
                    file_id,
                    export_mime,
                    save_path
                )

                continue

            # Normal file
            extension = os.path.splitext(file_name)[1]

            if extension == "":
                guessed = mimetypes.guess_extension(mime)
                if guessed:
                    file_name += guessed

            save_path = os.path.join(
                local_folder,
                file_name
            )

            print(f"⬇️ Downloading {file_name}")

            try:
                download_binary_file(
                    service,
                    file_id,
                    save_path
                )

            except Exception as e:
                print(f"❌ Failed: {file_name}")
                print(e)

        page_token = results.get("nextPageToken")

        if page_token is None:
            break
def main():

    print("🔐 Authenticating...")

    service = authenticate()

    print("✅ Connected to Google Drive")

    print("\n🚀 Starting Sync...\n")

    sync_folder(
        service,
        ROOT_FOLDER_ID,
        DOWNLOAD_DIR
    )

    print("\n🎉 Sync Complete!")


if __name__ == "__main__":
    main()