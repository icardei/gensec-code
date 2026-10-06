# Setup
```
gcloud services enable drive.googleapis.com
```

- Configure the OAuth consent screen: https://console.cloud.google.com/apis/credentials/consent.
- Under data access enable the Google Drive API.
- If you didn't create the app with the "internal" type then go to Audience and add a test user with your email.
- Create an OAuth Client ID for application type "Desktop App" https://console.cloud.google.com/apis/credentials/oauthclient.
- Upload the resulting JSON file to cloud shell.
```
gcloud compute scp client_secret_*.json kali-vm:/home/youruser/gensec-code/04_MCP/02_google_drive/credentials.json
```

On course-vm run `python auth.py` and open the URL. Once authorized you should see a list of Google Drive files in your console to confirm it's working.