from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import socket
import os

def build_gmail_user_credentials_for_api_calls():
    """
    This function builds gmail API service with credentials for API calls

    Returns: gmail API service with credentials
    """

    # If modifying these scopes, delete the file token.json.
    scopes = ["https://mail.google.com/"]

    # Force IPv4 (use original and forward parameters correctly)
    _orig_getaddrinfo = socket.getaddrinfo

    def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
        return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = _getaddrinfo_ipv4

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)

    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

    return service
