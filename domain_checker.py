# Import required libraries and custom modules
import requests
import os.path
import pandas as pd
from datetime import datetime
import credentials


def check_domain_location():
    file_path = 'C:\\Phishing Analysis\\domain_info.csv'
    if not os.path.exists(file_path):
        columns = ['Date', 'Domain', 'Status']
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
    return file_path


def check_domain_exists(csv_file, date, domain, status, source):
    date = str(date).strip()
    domain = domain.strip() if domain else domain
    status = status.strip() if status else status
    date = str(date).strip()
    exists = csv_file[
        (csv_file['Date'] == date) &
        (csv_file['Domain'] == domain) &
        (csv_file['Status'] == status)]
    # If domain already exists, return 1, otherwise, return 0
    if not exists.empty:
        return 1
    else:
        return 0


def extract_domain(domain):
    # Remove protocol if it presents
    if domain.startswith('http://'):
        domain = domain[7:]
    elif domain.startswith('https://'):
        domain = domain[8:]
    # If it's an email address, split and return the domain part
    if '@' in domain:
        domain = domain.split('@')[-1]
    # Remove any trailing slashes
    domain = domain.split('/')[0].strip()
    return domain


def domain_check(domain):
    domain = extract_domain(domain)
    path = check_domain_location()
    df = pd.read_csv(path)

    # Data for API
    api_key = credentials.api_key
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    # Parameters for the API request
    headers = {
        "x-apikey": api_key,
        "accept": "application/json"
    }

    current_date = datetime.now().strftime("%d/%m/%Y")
    # Make a request to VirusTotal
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from VirusTotal: {e}")
        return
    source = f"https://www.virustotal.com/api/v3/domains/{domain}"

    # Check the response
    if response.status_code == 200:
        result = response.json()
        # Check if the domain exists in the response
        if result['data']:
            malicious = result['data']['attributes']['last_analysis_stats']['malicious']
            # Determine if the domain is malicious or not
            if malicious > 0:
                status = "Malicious Domain"
            else:
                status = "Verified Domain"
        else:
            status = "Unscanned Domain"
    else:
        print(f"Error: {response.status_code} - {response.text}")
        status = "Unscanned Domain"

    if check_domain_exists(df, current_date, domain, status, source) == 0:
        # Create a new domain record
        new_row = {
            'Date': current_date if current_date else 'N/A',
            'Domain': domain if domain else 'N/A',
            'Status': status if status else 'N/A',
            'Source': source if source else 'N/A',
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
    return status
