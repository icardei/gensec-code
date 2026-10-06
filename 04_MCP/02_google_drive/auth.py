import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """
    Authenticate user for Google Drive API access.
    Returns credentials with automatic refresh capability.
    """
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'
    
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Token expired, refreshing...")
                creds.refresh(Request())
                print("Credentials refreshed successfully")
                # Save the refreshed credentials
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                    print(f"Updated credentials saved to {token_path}")
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Credentials file '{credentials_path}' not found. "
                    "Please download it from Google Cloud Console."
                )
            
            print("Getting new credentials...")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            print("New credentials obtained")
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                print(f"Credentials saved to {token_path}")
    else:
        # Check if token will expire soon (within 5 minutes) and refresh proactively
        if creds.expiry:
            time_until_expiry = creds.expiry - datetime.datetime.utcnow()
            if time_until_expiry.total_seconds() < 300:  # Less than 5 minutes
                try:
                    print("Token expires soon, refreshing proactively...")
                    creds.refresh(Request())
                    print("Credentials refreshed proactively")
                    # Save the refreshed credentials
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                        print(f"Updated credentials saved to {token_path}")
                except Exception as e:
                    print(f"Error proactively refreshing credentials: {e}")
    
    return creds

def get_drive_service():
    """
    Get authenticated Google Drive service object.
    """
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    return service

def check_token_status():
    """
    Check the current token status and expiration time.
    """
    token_path = 'token.json'
    
    if not os.path.exists(token_path):
        print("No token file found")
        return None
    
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if creds.expiry:
            now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)  # Use naive UTC time for comparison
            time_until_expiry = creds.expiry - now
            
            print(f"Token expires at: {creds.expiry} UTC")
            print(f"Current time: {now} UTC")
            
            if time_until_expiry.total_seconds() > 0:
                hours = time_until_expiry.total_seconds() // 3600
                minutes = (time_until_expiry.total_seconds() % 3600) // 60
                print(f"Time until expiry: {int(hours)}h {int(minutes)}m")
                
                if time_until_expiry.total_seconds() < 300:
                    print("⚠️  Token expires within 5 minutes!")
                elif time_until_expiry.total_seconds() < 3600:
                    print("⚠️  Token expires within 1 hour")
                else:
                    print("✅ Token is valid")
            else:
                print("❌ Token has expired")
        else:
            print("Token expiry information not available")
            
        print(f"Token valid: {creds.valid}")
        return creds
        
    except Exception as e:
        print(f"Error checking token status: {e}")
        return None

def test_authentication():
    """
    Test the authentication by listing files in Google Drive.
    """
    try:
        print("=== Token Status ===")
        check_token_status()
        print("\n=== Authenticating ===")
        
        service = get_drive_service()
        
        # List first 10 files
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        
        print("\n=== Google Drive Files ===")
        if not items:
            print('No files found in Google Drive.')
        else:
            print('Files in your Google Drive:')
            for item in items:
                print(f"- {item['name']} (ID: {item['id']})")
        
        print("\n✅ Authentication successful!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

if __name__ == "__main__":
    # Test authentication when run directly
    test_authentication()