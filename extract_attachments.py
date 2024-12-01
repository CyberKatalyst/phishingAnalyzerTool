# Import required libraries and custom modules
import hashlib


def extract_details(email_information):
    attachments = []
    # Loop through each attachment
    for attachment in email_information.attachments:
        # Get the filename and hash of the file
        filename = attachment.get('filename')
        file_content = attachment.get('payload').encode('utf-8')
        attachment_hash = hashlib.sha256(file_content).hexdigest()
        # Store the filename and hash in the attachments list
        attachments.append({
            'Filename': filename,
            'sha256': attachment_hash
        })
    return attachments

