# Import required libraries and custom modules
import os.path
import pandas as pd
import domain_checker
import mailparser
import detect_and_translate
import extract_links
import extract_attachments
import prediction
import url_checker

def check_record_location():
    file_path = 'C:\\Phishing Analysis\\analyzed_emails.csv'
    # If the file exists, then load it as DF
    if not os.path.exists(file_path):
        columns = ['Date', 'From', 'Domain validation', 'Subject', 'Body', 'Number of Attachments', 'Attachments',
                   'Number of Links', 'Links', 'Malicious Link Indicator', 'Suspicious Evidence', 'Email Classification']
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
    return file_path


def check_email_exists(csv_file, date, sender, subject):
    sender = sender.strip() if sender else ''
    date = str(date).strip()
    exists = csv_file[
        (csv_file['Date'].str.strip() == date) &
        (csv_file['From'].str.strip() == sender) &
        (csv_file['Subject'].str.strip() == subject)
    ]
    # If email already exists, return 1, otherwise, return 0
    if not exists.empty:
        return 1
    else:
        return 0


def get_info(email):
    # Get the path of the CSV file
    path = check_record_location()
    # Load the DataFrame
    df = pd.read_csv(path)
    try:
        email_info = mailparser.parse_from_file(email)
    except Exception as e:
        print(f"Error parsing email: {e}")
        return

    email_subject, email_body = detect_and_translate.parse_email_and_process_translation(email)
    email_prediction = prediction.predication(email_body)
    email_urls = extract_links.get_urls(email_info.body)
    email_sender = email_info.from_[0][1] if email_info.from_ else 'N/A'
    email_date = email_info.date if email_info.date else 'N/A'
    email_attachments = extract_attachments.extract_details(email_info)
    domain_validation_status = domain_checker.domain_check(email_sender)
    exist = check_email_exists(df, email_date, email_sender, email_subject)

    if exist == 0:
        # Create a new email record
        new_row = {
            'Date': email_date,
            'From': email_sender,
            'Domain validation': domain_validation_status,
            'Subject': email_subject,
            'Body': email_body,
            'Number of Attachments': len(email_info.attachments),
            'Attachments': email_attachments,
            'Number of Links': len(email_urls),
            'Links': email_urls,
            'Malicious Link Indicator': url_checker.url_check(email_urls),
            'Suspicious Evidence': None,
            'Email Classification': email_prediction,
        }

        try:
            # Convert the new email record to a DF
            new_record_df = pd.DataFrame([new_row])
            if df.empty:
                df = new_record_df
            else:
                df = pd.concat([df, new_record_df], ignore_index=True)
            # Save the updated DF back to the .csv file
            df.to_csv(path, index=False)
        except Exception as e:
            print(f"Error during the saving record: {e}")

