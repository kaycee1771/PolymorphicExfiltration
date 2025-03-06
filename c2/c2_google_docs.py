from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

class GoogleDocsC2:
    """
    C2 Client using Google Docs as a Command & Control server.
    - Reads the latest command from a shared Google Doc.
    """

    def __init__(self, doc_id, credentials_file="credentials.json"):
        self.doc_id = doc_id
        self.credentials_file = credentials_file
        self.service = self.authenticate_google_docs()

    def authenticate_google_docs(self):
        """ Authenticate with Google Docs API. """
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/documents.readonly"]
        )
        return build("docs", "v1", credentials=creds)

    def get_latest_command(self):
        """ Fetches the latest command from the Google Doc. """
        try:
            document = self.service.documents().get(documentId=self.doc_id).execute()
            content = document.get("body", {}).get("content", [])
            commands = [item["paragraph"]["elements"][0]["textRun"]["content"].strip()
                        for item in content if "paragraph" in item]
            return commands[-1] if commands else None
        except Exception as e:
            print(f"⚠️ C2 Error: {e}")
            return None

# Example Usage
if __name__ == "__main__":
    DOC_ID = "1ngLlijVCAuNEwv3FKzi3BI3VM6F9wKdUqTu4b73O26E"
    c2 = GoogleDocsC2(DOC_ID)

    while True:
        command = c2.get_latest_command()
        if command:
            print(f"📡 Received C2 Command: {command}")
        time.sleep(10)  # Check for new commands every 10 seconds
