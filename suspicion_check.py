import database
import vt
import base64
import credentials
import requests
from datetime import datetime
import logging
import whois
from colorama import Fore, Style, init
import parameters
import prediction
import rule

# Set up logging
logging.basicConfig(
    filename="suspicion_check_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def url_check(url_list):
    print("URL Analysis:")
    print("📝 VirusTotal Verification:")
    results = {}
    with vt.Client(credentials.api_key) as client:
        for url_to_check in url_list:
            url_id = base64.urlsafe_b64encode(url_to_check.encode()).decode().strip("=")
            try:
                url = client.get_object(f"/urls/{url_id}")
                url_analysis = url.last_analysis_stats

                if url_analysis['malicious'] > 0:
                    vt_status = "Malicious URL"
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] > 0:
                    vt_status = 'suspicious'
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] == 0 and url_analysis['malicious'] == 0 and url_analysis['undetected'] > url_analysis['harmless']:
                    vt_status = "undetected"
                    results.update({url_to_check: vt_status})
                elif url_analysis['suspicious'] == 0 and url_analysis['malicious'] == 0 and url_analysis['harmless'] > url_analysis['undetected']:
                    vt_status = "verified"
                    results.update({url_to_check: vt_status})
            except vt.error.APIError as e:
                if e.code == "NotFoundError":
                    vt_status = "not found"
                else:
                    vt_status = "Error"

            if "verified" in vt_status:
                icon = "✅"
            else:
                icon = "🔴"

            print(f" {icon} {url_to_check} is {vt_status}")
            database.create_url_db()
            database.add_to_table_url(url_to_check, vt_status)


def domain_check(domain):
    print("Domain Analysis:")

    domain_info = whois.whois(domain)

    # Initialize colorama for cross-platform compatibility
    init(autoreset=True)

    # Extract the domain status from WHOIS data
    domain_statuses = domain_info.get('status', [])

    # Check and print suspicious statuses
    found_suspicious = False

    print("🚦 Status:")
    for status in domain_statuses:
        for suspicious_status, description in parameters.status_descriptions.items():
            if suspicious_status in status:
                found_suspicious = True
                # Print the status in red and provide a description
                print(f" 🔴 Include suspicious keyword - {suspicious_status.upper()}. {description}")

    if not found_suspicious:
        print(f" 🟢 No suspicious keyword1"
              f" found for domain '{domain}'.")

    domain_creation_date = domain_info.creation_date
    if isinstance(domain_creation_date, list):
        domain_creation_date = domain_creation_date[0]
    domain_age = (datetime.now() - domain_creation_date).days

    print("⏳ Registration time: ")
    if domain_age < parameters.suspicious_threshold_domain:
        print(f" 🚨 The domain '{domain}' is {domain_age} days old, which is suspicious.")
    else:
        print(f" ✅ The domain '{domain}' is {domain_age} days old and appears to be less suspicious.")

    print("📝 Verification:")
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    # Parameters for the API request
    headers = {
        "x-apikey": credentials.api_key,
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.info(f"Error fetching data from VirusTotal: {e}")
        return

    # Check the response
    if response.status_code == 200:
        result = response.json()
        # Check if the domain exists in the response
        if result['data']:
            malicious = result['data']['attributes']['last_analysis_stats']['malicious']
            # Determine if the domain is malicious or not
            if malicious > 0:
                status = "malicious"
            else:
                status = "verified"
        else:
            status = "unscanned"
    else:
        logging.info(f"Error: {response.status_code} - {response.text}")
        status = "unscanned Domain"

    if "verified" in status:
        icon = "✅"
    else:
        icon = "🔴"

    print(f" {icon} {domain} is {status} according to VirusTotal.")
    database.create_domain_db()
    database.add_to_table_domain(domain, status)

    abuse_url = f"https://www.abuseipdb.com/check/{domain}"
    response = requests.get(abuse_url)

    if response.status_code == 200:
        print(f" 🔴 Domain {domain} is in the AbuseIPDB database.")
    else:
        print(f" ✅ Domain {domain} is not flagged in AbuseIPDB.")


def body_check(body):
    print(f"Body Analysis: ")
    print(f"⚖️ Rule-Based Check: ")
    if rule.rule_based_check(body):
        print(" 🔴 Based on the rule, the body is suspicious.")
    else:
        print(" ✅ Based on the rule, the body is safe.")
    print(f"⚠️ Anomaly Detection Check")
    prediction.anomaly_body_detection(body)