# Import required libraries and custom modules
import mailparser
import detect_and_translate
import database
import extract_links
import extract_attachments


def extract_info(email_path):
    print(f"The email {email_path} is being extracted ...\n")
    try:
        email_info = mailparser.parse_from_file(email_path)
    except Exception as expt:
        print(f"Error parsing email: {expt}")
        return

    email_subject, email_body = detect_and_translate.parse_email_and_process_translation(email_path)
    email_urls = extract_links.get_urls(email_info.body)
    email_sender = email_info.from_[0][1] if email_info.from_ else 'N/A'
    email_date = email_info.date if email_info.date else 'N/A'
    email_attachments = extract_attachments.extract_details(email_info)

    # Filter out URLs that contain the '@' symbol using list comprehension
    urls = [url for url in email_urls if '@' not in url]

    import_email_info_to_db(email_date, email_sender, email_subject, email_body, urls, email_attachments)

    return email_date, email_sender, email_subject, email_body, urls, email_attachments


def import_email_info_to_db(email_date, email_sender, email_subject, email_body, urls, email_attachments):
    # Ensure the DB and table are set up
    database.create_email_db()
    database.add_to_table_email(email_date, email_sender, email_subject, email_body, urls, email_attachments)


def extract_domain(email_address):
    # Remove protocol (http or https) if it exists
    if email_address.startswith('http://'):
        email_address = email_address[7:]  # Remove 'http://'
    elif email_address.startswith('https://'):
        email_address = email_address[8:]  # Remove 'https://'

    # If it's an email address, split and return the domain part
    if '@' in email_address:
        domain = email_address.split('@')[-1]  # Extract domain after '@'

    # Remove any trailing slashes (in case it's part of a URL)
    domain = domain.split('/')[0].strip()

    return domain
