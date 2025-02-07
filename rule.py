import re
from urllib.parse import urlparse


# General rule-based check for suspicious patterns
def rule_based_check(email_text):
    # Check for suspicious domains (long domain names, random-looking, or uncommon TLDs)
    if is_suspicious_domain(email_text):
        return True

    # Check for suspicious phrases (like password reset links)
    suspicious_phrases = ['reset your password', 'urgent action required', 'click this link', 'login', 'security alert']
    if any(phrase in email_text.lower() for phrase in suspicious_phrases):
        return True

    # Check for random-looking strings (alphanumeric sequences)
    random_string_pattern = r'\b[a-zA-Z0-9]{6,}\b'  # Matches 6 or more alphanumeric characters in a row
    if re.search(random_string_pattern, email_text):
        return True

    # Check for unusual greetings (e.g., random or generic names)
    if 'Hi ' in email_text and len(re.findall(r'\b[a-zA-Z0-9]{8,}\b', email_text)) > 0:
        return True

    return False


# Function to check if a domain is suspicious
def is_suspicious_domain(email_text):
    # Extract domains from email text using regular expressions
    domains = re.findall(r'@([a-zA-Z0-9.-]+)', email_text)

    # Loop through each domain and perform checks
    for domain in domains:
        # Check if the domain has random-looking characters
        if re.search(r'\d{10,}', domain) or len(domain) > 30:
            return True

        # Check for uncommon TLDs (this is just an example, feel free to expand the list)
        suspicious_tlds = ['.xyz', '.top', '.club', '.info', '.win', '.cc']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            return True

        # Optionally: Check for domains that are "too random"
        # Consider domains with a combination of alphanumeric strings and dots as suspicious
        if re.match(r'^[a-zA-Z0-9]{6,}\.[a-zA-Z]{2,}$', domain):  # e.g., `a1b2c3d4.com`
            return True

    return False


