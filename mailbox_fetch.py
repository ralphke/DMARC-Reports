"""Fetch DMARC report attachments from Exchange mailbox via Microsoft Graph API."""
import os
import base64
import json
from pathlib import Path
from datetime import datetime

import requests  # pip install requests
from dotenv import load_dotenv  # pip install python-dotenv
import msal  # pip install msal

# Load environment variables from .env file
load_dotenv()

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
MAILBOX_UPN = os.environ["MAILBOX_UPN"]

AUTHORITY = (
    f"https://login.microsoftonline.com/{TENANT_ID}"
)
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH = "https://graph.microsoft.com/v1.0"
BASE_DOWNLOAD_DIR = Path("./inbox")
PROCESSED_FILE = Path("./processed_messages.json")

# Load previously processed message IDs
processed_messages = set()
if PROCESSED_FILE.exists():
    with open(PROCESSED_FILE, "r", encoding="utf-8") as file_handle:
        processed_messages = set(json.load(file_handle))

app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)
TOKEN = app.acquire_token_for_client(scopes=SCOPE)
if not TOKEN or "access_token" not in TOKEN:
    raise ValueError("Failed to acquire access token. Check your credentials.")
HEADERS = {"Authorization": f"Bearer {TOKEN['access_token']}"}

# Filter for messages with attachments
# (process all, but skip already processed ones)
PARAMS = {
    "$filter": "hasAttachments eq true",
    "$select": "id,subject,receivedDateTime,from,hasAttachments",
    "$top": 999,  # Request maximum messages per page
}


def save_attachment(attachment, year_dir):
    """Save a single attachment to the specified year directory."""
    name = attachment["name"]
    is_target_file = any(
        name.lower().endswith(extension)
        for extension in (".zip", ".gz", ".xml")
    )
    if not is_target_file:
        return False

    binary_data = base64.b64decode(attachment["contentBytes"])
    output_path = year_dir / name

    # Skip if file already exists
    if output_path.exists():
        print(f"Skipped {output_path} (already exists)")
    else:
        with open(output_path, "wb") as output_file:
            output_file.write(binary_data)
        print(f"Saved {output_path}")
    return True


def process_message_attachments(message_id, year_dir):
    """Fetch and process all attachments for a given message."""
    attachment_response = requests.get(
        f"{GRAPH}/users/{MAILBOX_UPN}/messages/{message_id}/attachments",
        headers=HEADERS,
        timeout=30,
    )
    if attachment_response.status_code != 200:
        print(f"Warning: Could not fetch attachments for message {message_id}")
        return 0

    attachments = attachment_response.json()
    saved_count = 0

    for attachment in attachments.get("value", []):
        if attachment.get("@odata.type") == "#microsoft.graph.fileAttachment":
            if save_attachment(attachment, year_dir):
                saved_count += 1

    return saved_count


def fetch_and_process_attachments():
    """Main function to fetch DMARC attachments from mailbox."""
    next_link = f"{GRAPH}/users/{MAILBOX_UPN}/mailFolders/Inbox/messages"
    total_messages = 0
    total_attachments = 0

    while next_link:
        response = requests.get(
            next_link,
            headers=HEADERS,
            params=PARAMS if next_link.startswith(GRAPH) else None,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        messages = data.get("value", [])
        total_messages += len(messages)
        print(
            f"Processing {len(messages)} messages... "
            f"(Total so far: {total_messages})"
        )

        for message in messages:
            message_id = message["id"]

            # Skip if already processed
            if message_id in processed_messages:
                continue

            received_dt = datetime.fromisoformat(
                message["receivedDateTime"].replace("Z", "+00:00")
            )
            year = received_dt.year

            # Create year-specific directory
            year_dir = BASE_DOWNLOAD_DIR / str(year)
            year_dir.mkdir(parents=True, exist_ok=True)

            # Process attachments for this message
            saved_count = process_message_attachments(message_id, year_dir)

            # Add to processed list if any attachments were saved
            if saved_count > 0:
                total_attachments += saved_count
                processed_messages.add(message_id)
                subject = message.get("subject", "No subject")[:60]
                print(f"✓ Marked as processed: {subject}")

        # Get next page of results
        next_link = data.get("@odata.nextLink")
        if next_link:
            print("Fetching next page...")

    # Save processed message IDs
    with open(PROCESSED_FILE, "w", encoding="utf-8") as output_file:
        json.dump(list(processed_messages), output_file, indent=2)

    print(
        f"\nComplete! Processed {total_messages} messages and "
        f"saved {total_attachments} new attachments."
    )
    print(f"Total processed messages tracked: {len(processed_messages)}")


if __name__ == "__main__":
    fetch_and_process_attachments()
