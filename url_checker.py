# Import required libraries and custom modules
import vt
import base64
import os
import pandas as pd
from datetime import datetime


def check_url_location():
    file_path = 'C:\\Phishing Analysis\\url_info.csv'
    if not os.path.exists(file_path):
        columns = ['Date', 'URL', 'Status']
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
    return file_path


def check_url_exists(csv_file, date, url, status):
    date = str(date).strip()
    status = status.strip() if status else status
    date = str(date).strip()
    exists = csv_file[
        (csv_file['Date'] == date) &
        (csv_file['URL'] == url) &
        (csv_file['Status'] == status)]
    # If domain already exists, return 1, otherwise, return 0
    if not exists.empty:
        return 1
    else:
        return 0


def url_check(urls):
    path = check_url_location()
    df = pd.read_csv(path)
    results = {}
    with vt.Client("XXX") as client:
        for url_to_check in urls:
            url_id = base64.urlsafe_b64encode(url_to_check.encode()).decode().strip("=")
            try:
                url = client.get_object(f"/urls/{url_id}")
                url_analysis = url.last_analysis_stats

                current_date = datetime.now().strftime("%d/%m/%Y")

                if url_analysis['malicious'] > 0:
                    vt_status = "Malicious URL"
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] > 0:
                    vt_status = 'Suspicious URL'
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] == 0 and url_analysis['malicious'] == 0 and url_analysis['undetected'] > url_analysis['harmless']:
                    vt_status = "Undetected URL"
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] == 0 and url_analysis['malicious'] == 0 and url_analysis['harmless'] > url_analysis['undetected']:
                    vt_status = "Verified URL"
                    results.update({url_to_check: vt_status})
            except vt.error.APIError as e:
                if e.code == "NotFoundError":
                    vt_status = "Not Found"
                else:
                    vt_status = "Error"

            if check_url_exists(df, current_date, url_to_check, vt_status) == 0:
                # Create a new domain record
                new_row = {
                    'Date': current_date if current_date else 'N/A',
                    'URL': url_to_check if url else 'N/A',
                    'Status': vt_status if vt_status else 'N/A',
                }

                try:
                    # Convert the new domain record to a DF
                    new_row_df = pd.DataFrame([new_row])
                    if df.empty:
                        df = new_row_df
                    else:
                        df = pd.concat([df, new_row_df], ignore_index=True)
                    # Save the updated Df back to the .csv file
                    df.to_csv(path, index=False)
                except Exception as e:
                    print(f"Error during the saving record : {e}")
        return results


