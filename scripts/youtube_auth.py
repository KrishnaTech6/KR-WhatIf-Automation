"""One-time YouTube login for the pipeline. Run it on your own computer, once.

  pip install google-auth-oauthlib
  python youtube_auth.py client_secret.json

client_secret.json = the file you downloaded for the Desktop OAuth client.
A browser opens: pick the account that owns KR's What If Explained, then
Advanced -> Go to KR What If Uploader (unsafe) -> Allow.
It prints 3 values; save each as a GitHub secret with exactly that name.
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",     # upload videos
    "https://www.googleapis.com/auth/youtube.force-ssl",  # thumbnails, titles, comments
]

if len(sys.argv) != 2:
    sys.exit("usage: python youtube_auth.py client_secret.json")

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
if not creds.refresh_token:
    sys.exit("No refresh token came back. Remove the app at https://myaccount.google.com/permissions and run again.")

client = json.load(open(sys.argv[1]))
client = client.get("installed") or client.get("web")
print("\nSave these 3 as GitHub secrets (repo Settings -> Secrets and variables -> Actions):\n")
print("YT_CLIENT_ID     =", client["client_id"])
print("YT_CLIENT_SECRET =", client["client_secret"])
print("YT_REFRESH_TOKEN =", creds.refresh_token)
